# --- Clothing Product Analysis ---

import requests
import json
from bs4 import BeautifulSoup

def analyze_product_url(url):
    """
    Analyze a clothing product URL, extract details, find similar items, and list sales.
    Always returns keys: 'similar_products', 'error' (if any), and 'product_info'.
    """
    scraperapi_key = ""
    api_url = f"https://api.scraperapi.com/?api_key={scraperapi_key}&url={url}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return {
                "error": "Failed to fetch product page",
                "similar_products": [],
                "product_info": {}
            }
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        # Try to extract product info (simulate, since real selectors vary)
        try:
            name = soup.find(class_="product-name")
            price = soup.find(class_="price")
            product_info = {
                "name": name.get_text(strip=True) if name else None,
                "price": price.get_text(strip=True) if price else None
            }
        except Exception:
            product_info = {}

        # Find similar products: Prefer .similar-products section if present
        similar_products = []
        similar_section = soup.find(class_="similar-products")
        if similar_section:
            for prod in similar_section.find_all("a", href=True):
                href = prod["href"]
                text = prod.get_text().strip()
                price_tag = prod.find_next("span", class_="price")
                price = price_tag.get_text(strip=True) if price_tag else None
                if len(text) > 2:
                    similar_products.append({"name": text, "url": href, "price": price})
        else:
            # fallback: all product links
            links = set()
            for a in soup.find_all("a", href=True):
                href = a["href"]
                text = a.get_text().strip()
                if (
                    href.startswith("http") and
                    "product" in href.lower() and
                    len(text) > 2 and
                    not any(x in href for x in ["facebook", "twitter", "instagram", "pinterest", "cart", "login", "signup"])
                ):
                    links.add(href)
            similar_products = [{"url": l} for l in list(links)[:5]]

        # If no product info and no similar products, treat as parsing error
        if not product_info.get("name") and not similar_products:
            return {
                "error": "Failed to parse product information",
                "similar_products": [],
                "product_info": {}
            }
        return {
            "product_info": product_info,
            "similar_products": similar_products,
            "upcoming_sales": []
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch product page: {str(e)}",
            "similar_products": [],
            "product_info": {}
        }
