import asyncio
import json
import random
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
from app.core.config import get_settings

settings = get_settings()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

class AlibabaScraper:
    """Production-ready Alibaba scraper based on scraper-bank/Alibaba.com-Scrapers.
    
    Uses Playwright with stealth configurations and proxy rotation.
    Swapped ScrapeOps proxy integration for Bright Data credentials.
    """
    
    def __init__(self):
        self.proxy_config = None
        if settings.BRIGHT_DATA_USER and settings.BRIGHT_DATA_PASS:
            self.proxy_config = {
                "server": settings.BRIGHT_DATA_PROXY,
                "username": settings.BRIGHT_DATA_USER,
                "password": settings.BRIGHT_DATA_PASS,
            }
    
    async def search_products(
        self,
        keyword: str,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """Search Alibaba for products matching keyword."""
        search_url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={keyword.replace(' ', '+')}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=settings.PLAYWRIGHT_HEADLESS,
                proxy=self.proxy_config,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                    "--disable-plugins",
                ]
            )
            
            context = await browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={"width": 1366 + random.randint(-100, 100), "height": 768 + random.randint(-50, 50)},
                locale="en-US",
                timezone_id="America/New_York",
            )
            
            # Inject stealth script
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                window.chrome = { runtime: {} };
            """)
            
            page = await context.new_page()
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(2.0, 4.0))
                
                # Handle potential CAPTCHA or blocking
                if await self._is_blocked(page):
                    raise Exception("Alibaba blocked the request (CAPTCHA or bot detection)")
                
                # Extract product cards
                product_cards = await page.query_selector_all('.card-info-list .list-no-v2')
                if not product_cards:
                    product_cards = await page.query_selector_all('[data-content="productItem"]')
                
                products = []
                for card in product_cards[:max_results]:
                    product = await self._extract_product_card(card)
                    if product:
                        products.append(product)
                
                # Get best product details
                best_product = products[0] if products else None
                if best_product and best_product.get("detail_url"):
                    detail = await self._get_product_detail(page, best_product["detail_url"])
                    best_product.update(detail)
                
                return {
                    "products": products,
                    "unit_price_usd": best_product.get("price_usd") if best_product else None,
                    "moq": best_product.get("moq") if best_product else None,
                    "supplier_rating": best_product.get("supplier_rating") if best_product else None,
                    "lead_time_days": best_product.get("lead_time_days") if best_product else None,
                    "scraped_at": json.dumps({}),
                    "search_keyword": keyword,
                }
                
            except PlaywrightTimeout:
                return {"error": "Timeout loading Alibaba", "products": []}
            finally:
                await browser.close()
    
    async def _is_blocked(self, page) -> bool:
        title = await page.title()
        return "captcha" in title.lower() or "verify" in title.lower()
    
    async def _extract_product_card(self, card) -> Optional[dict]:
        try:
            title_el = await card.query_selector('.elements-title-normal__content')
            title = await title_el.inner_text() if title_el else ""
            
            price_el = await card.query_selector('.elements-offer-price-normal__price')
            price_text = await price_el.inner_text() if price_el else ""
            price_usd = self._parse_price(price_text)
            
            moq_el = await card.query_selector('.elements-offer-price-normal__units')
            moq_text = await moq_el.inner_text() if moq_el else ""
            moq = self._parse_moq(moq_text)
            
            link_el = await card.query_selector('a')
            detail_url = await link_el.get_attribute("href") if link_el else ""
            if detail_url and not detail_url.startswith("http"):
                detail_url = "https:" + detail_url
            
            img_el = await card.query_selector('img')
            image_url = await img_el.get_attribute("src") if img_el else ""
            
            supplier_el = await card.query_selector('.company-name')
            supplier = await supplier_el.inner_text() if supplier_el else ""
            
            return {
                "title": title.strip(),
                "price_usd": price_usd,
                "moq": moq,
                "detail_url": detail_url,
                "image_url": image_url,
                "supplier": supplier.strip(),
            }
        except Exception:
            return None
    
    async def _get_product_detail(self, page, url: str) -> dict:
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(random.uniform(1.5, 3.0))
            
            # Extract additional details from product page
            rating_el = await page.query_selector('.company-header-score .score')
            rating_text = await rating_el.inner_text() if rating_el else ""
            rating = float(rating_text) if rating_text else None
            
            lead_time_el = await page.query_selector('.delivery-time')
            lead_time_text = await lead_time_el.inner_text() if lead_time_el else ""
            lead_time = self._parse_lead_time(lead_time_text)
            
            shipping_el = await page.query_selector('.shipping-amount')
            shipping_text = await shipping_el.inner_text() if shipping_el else ""
            shipping_cost = self._parse_price(shipping_text)
            
            return {
                "supplier_rating": rating,
                "lead_time_days": lead_time,
                "shipping_cost_usd": shipping_cost,
            }
        except Exception:
            return {}
    
    def _parse_price(self, text: str) -> Optional[float]:
        import re
        numbers = re.findall(r'[\d,]+\.?\d*', text.replace(",", ""))
        return float(numbers[0]) if numbers else None
    
    def _parse_moq(self, text: str) -> Optional[int]:
        import re
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else None
    
    def _parse_lead_time(self, text: str) -> Optional[int]:
        import re
        numbers = re.findall(r'(\d+).*day', text.lower())
        return int(numbers[0]) if numbers else None
