import httpx
import json
import re
from typing import Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings

settings = get_settings()

class MiniMaxClient:
    def __init__(self):
        self.api_key = settings.MINIMAX_API_KEY
        self.group_id = settings.MINIMAX_GROUP_ID
        self.base_url = settings.MINIMAX_BASE_URL
        self.model = settings.MINIMAX_MODEL
        self.max_tokens = settings.MINIMAX_MAX_TOKENS
        self.temperature = settings.MINIMAX_TEMPERATURE
        self.top_p = settings.MINIMAX_TOP_P
        self.timeout = settings.MINIMAX_TIMEOUT_SECONDS
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        response_format: Optional[dict] = None
    ) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
        
        if response_format:
            body["response_format"] = response_format
        
        url = f"{self.base_url}/text/chatcompletion_v2?GroupId={self.group_id}"
        response = await self.client.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        
        return {
            "content": data["choices"][0]["message"]["content"],
            "usage": data.get("usage", {}),
            "finish_reason": data["choices"][0].get("finish_reason")
        }
    
    async def analyze_product(self, product_data: dict) -> dict:
        system_prompt = """You are an expert e-commerce product analyst with deep knowledge of dropshipping, Amazon FBA, and Shopify markets in South Asia and globally.

CRITICAL INSTRUCTIONS:
- Always respond with ONLY valid JSON, no markdown, no explanation
- Be conservative in profit margin estimates
- Base your verdict strictly on the data provided
- If data is insufficient, flag it explicitly in the response"""

        user_message = f"""Analyze this e-commerce product opportunity and return a JSON verdict.

INPUT DATA:
{json.dumps(product_data, indent=2, ensure_ascii=False)}

RETURN EXACTLY THIS JSON STRUCTURE:
{{
  "verdict": "pursue" | "risky" | "skip",
  "confidence_score": <0-100>,
  "product_score": <0-100>,
  "score_breakdown": {{
    "profit_margin_score": <0-30>,
    "ad_momentum_score": <0-25>,
    "review_sentiment_score": <0-20>,
    "demand_trend_score": <0-15>,
    "competition_score": <0-10>
  }},
  "estimated_profit_margin_pct": <number>,
  "suggested_selling_price_usd": <number>,
  "suggested_ad_budget_monthly_usd": <number>,
  "main_risk": "<string>",
  "opportunity_summary": "<2-3 sentences>",
  "top_3_alternatives": ["<product1>", "<product2>", "<product3>"],
  "data_quality_warnings": ["<warning if any>"],
  "payback_period_days": <number>
}}"""

        result = await self.complete(
            system_prompt=system_prompt,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(result["content"])
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', result["content"], re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError("MiniMax returned non-JSON response")
    
    async def extract_themes(self, negative_reviews: list[str]) -> dict:
        if not negative_reviews:
            return {"complaints": [], "praises": []}
        
        system_prompt = "Extract top complaint themes from negative product reviews. Return ONLY JSON."
        user_message = f"""From these negative reviews, extract the top 5 complaint themes and top 3 praise themes (if any mixed sentiment).

REVIEWS:
{json.dumps(negative_reviews[:20], indent=2)}

RETURN JSON:
{{
  "complaints": ["theme1", "theme2", ...],
  "praises": ["theme1", "theme2", ...]
}}"""
        
        result = await self.complete(system_prompt=system_prompt, user_message=user_message)
        try:
            return json.loads(result["content"])
        except json.JSONDecodeError:
            return {"complaints": [], "praises": []}
    
    async def close(self):
        await self.client.aclose()
