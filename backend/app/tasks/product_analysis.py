import json
import asyncio
from datetime import datetime
from celery import shared_task, chain, group
from app.tasks.celery_app import celery_app
from app.core.config import get_settings
from app.services.scrapers.facebook_scraper import FacebookAdScraper
from app.services.scrapers.alibaba_scraper import AlibabaScraper
from app.services.scrapers.amazon_scraper import AmazonPAAPI, AmazonFallbackScraper
from app.services.scrapers.google_trends_scraper import GoogleTrendsScraper
from app.services.scrapers.circuit_breaker import fb_circuit, alibaba_circuit, amazon_circuit, google_trends_circuit
from app.services.ai.minimax_client import MiniMaxClient
from app.services.nlp.sentiment_analyzer import ReviewSentimentAnalyzer
from app.core.database import AsyncSessionLocal
from app.models.models import Product, AnalysisJob

settings = get_settings()

async def run_scrapers(product_name: str, target_market: str):
    """Run all scrapers in parallel with circuit breaker protection."""
    
    fb_scraper = FacebookAdScraper()
    alibaba_scraper = AlibabaScraper()
    amazon_api = AmazonPAAPI()
    trends_scraper = GoogleTrendsScraper()
    
    results = {}
    
    # Facebook Ads
    try:
        fb_data = await fb_circuit.call(
            fb_scraper.search_ads,
            search_terms=product_name,
            countries=[target_market]
        )
        results["facebook"] = fb_data
    except Exception as e:
        results["facebook"] = {"error": str(e)}
    
    # Alibaba
    try:
        alibaba_data = await alibaba_circuit.call(
            alibaba_scraper.search_products,
            keyword=product_name
        )
        results["alibaba"] = alibaba_data
    except Exception as e:
        results["alibaba"] = {"error": str(e)}
    
    # Amazon (primary PA API, fallback to HTML scraper)
    try:
        amazon_data = await amazon_circuit.call(
            amazon_api.search_items,
            keywords=product_name
        )
        if amazon_data.get("fallback_needed"):
            fallback = AmazonFallbackScraper()
            amazon_data = await fallback.search_items(product_name)
            await fallback.close()
        results["amazon"] = amazon_data
    except Exception as e:
        results["amazon"] = {"error": str(e)}
    
    # Google Trends
    try:
        trends_data = await google_trends_circuit.call(
            trends_scraper.get_interest_over_time,
            keywords=[product_name]
        )
        results["google_trends"] = trends_data
    except Exception as e:
        results["google_trends"] = {"error": str(e)}
    
    # Cleanup
    await fb_scraper.close()
    await amazon_api.close()
    
    return results

async def run_analysis_chain(scraped_data: dict) -> dict:
    """3-pass MiniMax M2.7 analysis chain."""
    
    client = MiniMaxClient()
    
    try:
        # Pass 1: Raw Data Normalization
        system_prompt = "Normalize messy scraped e-commerce data into clean structured JSON. Return ONLY JSON."
        user_message = f"Normalize this data:\n{json.dumps(scraped_data, indent=2)}"
        
        pass1 = await client.complete(
            system_prompt=system_prompt,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        normalized = json.loads(pass1["content"])
        
        # Pass 2: Competitive Intelligence
        system_prompt = "Analyze competitive landscape from normalized product data. Return ONLY JSON."
        user_message = f"Analyze competition:\n{json.dumps(normalized, indent=2)}"
        
        pass2 = await client.complete(
            system_prompt=system_prompt,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        competitive = json.loads(pass2["content"])
        
        # Pass 3: Final Verdict
        combined = {
            "normalized_data": normalized,
            "competitive_analysis": competitive
        }
        
        verdict = await client.analyze_product(combined)
        
        await client.close()
        return verdict
        
    except Exception as e:
        await client.close()
        return {"error": str(e), "verdict": "skip", "confidence_score": 0}

@celery_app.task(bind=True, max_retries=3)
def analyze_product_task(self, job_id: str, tenant_id: str, product_name: str, target_market: str, selling_platform: str = "amazon"):
    """Orchestrates the full analysis pipeline."""
    
    async def _run():
        # Update job status: starting
        await _update_job(job_id, "processing", "starting", 5)
        
        # Step 1: Parallel scraping
        await _update_job(job_id, "processing", "scraping_data", 15)
        scraped = await run_scrapers(product_name, target_market)
        
        # Step 2: NLP sentiment (if review data available)
        await _update_job(job_id, "processing", "nlp_sentiment", 40)
        sentiment = {"positive_pct": 0, "negative_pct": 0, "neutral_pct": 0}
        
        # Step 3: MiniMax Analysis
        await _update_job(job_id, "processing", "minimax_analysis", 60)
        analysis = await run_analysis_chain(scraped)
        
        # Step 4: Save result
        await _update_job(job_id, "processing", "saving", 90)
        product = await _save_product(tenant_id, product_name, target_market, selling_platform, scraped, analysis, sentiment)
        
        await _update_job(job_id, "completed", "done", 100, product_id=str(product.id))
        
        return {
            "product_id": str(product.id),
            "verdict": analysis.get("verdict"),
            "score": analysis.get("product_score"),
        }
    
    try:
        return asyncio.run(_run())
    except Exception as exc:
        self.retry(exc=exc, countdown=2 ** self.request.retries)

async def _update_job(job_id: str, status: str, step: str, percent: int, product_id: str = None, error: str = None):
    """Update analysis job status in database."""
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        result = await db.execute(select(AnalysisJob).where(AnalysisJob.id == job_id))
        job = result.scalar_one_or_none()
        if job:
            job.status = status
            job.current_step = step
            job.progress_pct = percent
            if product_id:
                job.product_id = product_id
            if error:
                job.error_message = error
            if status == "completed":
                job.completed_at = datetime.utcnow()
            await db.commit()

async def _save_product(tenant_id, product_name, target_market, selling_platform, scraped, analysis, sentiment):
    """Save analysis result to database."""
    async with AsyncSessionLocal() as db:
        fb = scraped.get("facebook", {})
        ali = scraped.get("alibaba", {})
        amz = scraped.get("amazon", {})
        gt = scraped.get("google_trends", {})
        
        product = Product(
            tenant_id=tenant_id,
            product_name=product_name,
            target_market=target_market,
            selling_platform=selling_platform,
            facebook_ads_data=fb,
            alibaba_data=ali,
            amazon_data=amz,
            google_trends_data=gt,
            active_ads_count=fb.get("active_ads_count"),
            avg_ad_duration_days=fb.get("avg_duration_days"),
            alibaba_unit_price=ali.get("unit_price_usd"),
            alibaba_moq=ali.get("moq"),
            amazon_avg_price=amz.get("avg_selling_price_usd"),
            avg_rating=amz.get("avg_rating"),
            review_count=amz.get("total_reviews"),
            sentiment_positive_pct=sentiment.get("positive_pct"),
            sentiment_negative_pct=sentiment.get("negative_pct"),
            verdict=analysis.get("verdict"),
            product_score=analysis.get("product_score"),
            confidence_score=analysis.get("confidence_score"),
            score_breakdown=analysis.get("score_breakdown"),
            ai_analysis_full=analysis,
            facebook_scraped_at=datetime.utcnow() if not fb.get("error") else None,
            alibaba_scraped_at=datetime.utcnow() if not ali.get("error") else None,
            amazon_scraped_at=datetime.utcnow() if not amz.get("error") else None,
        )
        
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
