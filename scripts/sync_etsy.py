#!/usr/bin/env python3
"""Synchronise public Etsy listing data into the Lasair catalogue overlay."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import html
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


API_BASE = "https://api.etsy.com/v3/application"
SHOP_NAME = "LasairStudio"
SITE_ORIGIN = "https://www.lasair-studios.co.uk"
ROOT = Path(__file__).resolve().parents[1]
APP_FILE = ROOT / "app.js"
OUTPUT_FILE = ROOT / "etsy-products.js"
INDEX_FILE = ROOT / "index.html"
PRODUCTS_DIR = ROOT / "products"
SITEMAP_FILE = ROOT / "sitemap.xml"


def api_credentials() -> str:
    raw = os.environ.get("ETSY_CREDENTIALS", "").strip()
    if not raw:
        raise RuntimeError("ETSY_CREDENTIALS is not configured")
    if ":" in raw:
        return raw
    parts = raw.split()
    if len(parts) == 2:
        return f"{parts[0]}:{parts[1]}"
    raise RuntimeError(
        "LASAIR_STUDIOS_ETSY must contain the Etsy keystring and shared secret separated by a colon"
    )


def api_get(path: str, credentials: str, **params: object) -> object:
    query = f"?{urlencode(params, doseq=True)}" if params else ""
    request = Request(
        f"{API_BASE}{path}{query}",
        headers={
            "Accept": "application/json",
            "User-Agent": "LasairStudioWebsiteSync/1.0",
            "x-api-key": credentials,
        },
    )
    for attempt in range(4):
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code == 429 or error.code >= 500:
                if attempt < 3:
                    retry_after = int(error.headers.get("retry-after", "0") or 0)
                    time.sleep(max(retry_after, 2**attempt))
                    continue
            detail = ""
            try:
                error_payload = json.loads(error.read().decode("utf-8"))
                detail = str(error_payload.get("error") or error_payload.get("message") or "").strip()
            except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
                pass
            suffix = f": {detail}" if detail else ""
            raise RuntimeError(
                f"Etsy API request to {path} failed with HTTP {error.code}{suffix}"
            ) from error
        except URLError as error:
            if attempt < 3:
                time.sleep(2**attempt)
                continue
            raise RuntimeError("Etsy API request failed after retries") from error
    raise RuntimeError("Etsy API request failed")


def curated_ids() -> list[str]:
    source = APP_FILE.read_text(encoding="utf-8")
    ids = re.findall(r"\bid:\s*'(\d+)'", source)
    if not ids:
        raise RuntimeError("No curated product IDs were found in app.js")
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate curated product IDs were found in app.js")
    return ids


def curated_etsy_urls() -> dict[str, str]:
    source = APP_FILE.read_text(encoding="utf-8")
    pairs = re.findall(r"\bid:\s*'(\d+)'.*?\betsy:\s*'([^']+)'", source, re.DOTALL)
    return dict(pairs)


def find_shop_id(credentials: str) -> int:
    payload = api_get("/shops", credentials, shop_name=SHOP_NAME, limit=100)
    matches = [
        shop for shop in payload.get("results", [])
        if str(shop.get("shop_name", "")).casefold() == SHOP_NAME.casefold()
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one exact Etsy shop match for {SHOP_NAME}; found {len(matches)}")
    return int(matches[0]["shop_id"])


def active_listings(shop_id: int, credentials: str) -> list[dict[str, object]]:
    listings: list[dict[str, object]] = []
    offset = 0
    while True:
        payload = api_get(
            f"/shops/{shop_id}/listings/active",
            credentials,
            limit=100,
            offset=offset,
        )
        batch = payload.get("results", [])
        listings.extend(batch)
        offset += len(batch)
        if not batch or offset >= int(payload.get("count", len(listings))):
            break
    if not listings:
        raise RuntimeError("Etsy returned no active listings; refusing to replace catalogue data")
    return listings


def format_price(listing: dict[str, object]) -> str | None:
    money = listing.get("price")
    if not isinstance(money, dict):
        return None
    divisor = int(money.get("divisor") or 100)
    amount = int(money.get("amount") or 0)
    if divisor <= 0 or amount <= 0:
        return None
    currency = str(money.get("currency_code") or "GBP").upper()
    symbols = {"GBP": "£", "EUR": "€", "USD": "$"}
    value = amount / divisor
    formatted = f"{symbols.get(currency, currency + ' ')}{value:.2f}"
    if listing.get("has_variations"):
        return f"From {formatted}"
    return formatted


def listing_images(listing_id: str, credentials: str) -> list[str]:
    payload = api_get(f"/listings/{listing_id}/images", credentials)
    images = sorted(payload.get("results", []), key=lambda image: int(image.get("rank") or 0))
    urls = []
    for image in images:
        url = str(image.get("url_fullxfull") or image.get("url_570xN") or "")
        if url.startswith("https://i.etsystatic.com/"):
            urls.append(url)
    return urls


def build_catalogue(
    credentials: str,
) -> tuple[dict[str, dict[str, object]], list[dict[str, object]], dict[str, list[str]], int]:
    ids = curated_ids()
    shop_id = find_shop_id(credentials)
    listings = active_listings(shop_id, credentials)
    by_id = {str(listing["listing_id"]): listing for listing in listings}
    images_by_id = {
        listing_id: listing_images(listing_id, credentials)
        for listing_id in by_id
    }
    overlay: dict[str, dict[str, object]] = {}

    for listing_id in ids:
        listing = by_id.get(listing_id)
        if not listing:
            overlay[listing_id] = {"active": False}
            continue
        updated: dict[str, object] = {
            "active": True,
            "name": str(listing.get("title") or "").strip(),
            "description": str(listing.get("description") or "").strip(),
        }
        price = format_price(listing)
        if price:
            updated["price"] = price
        images = images_by_id[listing_id]
        if images:
            updated["images"] = images
        if not updated["name"] or not updated["description"]:
            raise RuntimeError(f"Listing {listing_id} is missing a title or description")
        overlay[listing_id] = updated

    new_listing_count = len(set(by_id) - set(ids))
    return overlay, listings, images_by_id, new_listing_count


def truncate_text(value: str, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    shortened = compact[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,.;:-")
    return f"{shortened}…"


def updated_date(listing: dict[str, object]) -> str | None:
    for field in ("updated_timestamp", "last_modified_timestamp", "original_creation_timestamp"):
        timestamp = listing.get(field)
        if timestamp:
            return datetime.fromtimestamp(int(timestamp), tz=UTC).date().isoformat()
    return None


def public_etsy_url(listing: dict[str, object], curated_urls: dict[str, str]) -> str:
    listing_id = str(listing["listing_id"])
    if listing_id in curated_urls:
        return curated_urls[listing_id]
    raw_url = str(listing.get("url") or "").strip()
    parsed = urlsplit(raw_url)
    if parsed.scheme == "https" and parsed.netloc.endswith("etsy.com") and parsed.path.startswith("/listing/"):
        return f"https://lasairstudio.etsy.com/uk{parsed.path}"
    return f"https://lasairstudio.etsy.com/uk/listing/{listing_id}"


def seo_products(
    listings: list[dict[str, object]], images_by_id: dict[str, list[str]]
) -> list[dict[str, object]]:
    curated_urls = curated_etsy_urls()
    products = []
    for listing in listings:
        listing_id = str(listing["listing_id"])
        name = str(listing.get("title") or "").strip()
        description = str(listing.get("description") or "").strip()
        if not name or not description:
            raise RuntimeError(f"Listing {listing_id} is missing a title or description")
        products.append(
            {
                "id": listing_id,
                "name": name,
                "description": description,
                "meta_description": truncate_text(description, 155),
                "seo_title": f"{truncate_text(name, 44)} | Lasair Studios",
                "price": format_price(listing),
                "price_amount": price_amount(listing),
                "currency": price_currency(listing),
                "images": images_by_id.get(listing_id, []),
                "etsy": public_etsy_url(listing, curated_urls),
                "updated": updated_date(listing),
            }
        )
    return sorted(products, key=lambda product: str(product["id"]))


def price_amount(listing: dict[str, object]) -> str | None:
    money = listing.get("price")
    if not isinstance(money, dict):
        return None
    divisor = int(money.get("divisor") or 100)
    amount = int(money.get("amount") or 0)
    if divisor <= 0 or amount <= 0:
        return None
    return f"{amount / divisor:.2f}"


def price_currency(listing: dict[str, object]) -> str:
    money = listing.get("price")
    if isinstance(money, dict):
        return str(money.get("currency_code") or "GBP").upper()
    return "GBP"


def render_product_page(product: dict[str, object]) -> str:
    product_id = str(product["id"])
    canonical = f"{SITE_ORIGIN}/products/{product_id}/"
    name = html.escape(str(product["name"]), quote=True)
    title = html.escape(str(product["seo_title"]), quote=True)
    description = html.escape(str(product["description"]), quote=False)
    meta_description = html.escape(str(product["meta_description"]), quote=True)
    etsy_url = html.escape(str(product["etsy"]), quote=True)
    price = html.escape(str(product.get("price") or "View price on Etsy"), quote=False)
    images = [str(image) for image in product.get("images", [])]
    primary_image = images[0] if images else f"{SITE_ORIGIN}/assets/branding/cow-logo.png"
    image_markup = "".join(
        f'<figure><img src="{html.escape(image, quote=True)}" alt="{name}" loading="lazy"></figure>'
        for image in images[:4]
    )
    schema: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": str(product["name"]),
        "description": str(product["meta_description"]),
        "image": images,
        "url": canonical,
        "sku": product_id,
        "brand": {"@type": "Brand", "name": "Lasair Studios"},
    }
    if product.get("price_amount"):
        schema["offers"] = {
            "@type": "Offer",
            "url": str(product["etsy"]),
            "priceCurrency": str(product["currency"]),
            "price": str(product["price_amount"]),
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
        }
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="product">
  <meta property="og:site_name" content="Lasair Studios">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{html.escape(primary_image, quote=True)}">
  <link rel="preconnect" href="https://i.etsystatic.com">
  <link rel="stylesheet" href="../../styles.css?v=20261029-1">
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="product-page-body">
  <header class="site-header product-page-header">
    <a class="brand brand-header" href="../../" aria-label="Lasair Studios home">
      <img class="brand-cow brand-cow-header" src="../../assets/branding/cow-logo-transparent.png" alt="Lasair Studios Highland cow logo">
    </a>
    <nav aria-label="Main navigation">
      <a href="../../#collection">Collection</a>
      <a href="../../#story">Our craft</a>
      <a class="nav-etsy" href="https://www.etsy.com/uk/shop/LasairStudio" target="_blank" rel="noopener">Visit Etsy <span aria-hidden="true">↗</span></a>
    </nav>
  </header>
  <main class="product-page-main">
    <a class="product-page-back" href="../../#collection">← Back to the collection</a>
    <article class="product-page-layout">
      <div class="product-page-gallery">{image_markup}</div>
      <div class="product-page-copy">
        <p class="eyebrow">Handmade in Scotland</p>
        <h1>{name}</h1>
        <p class="dialog-price">{price}</p>
        <div class="product-page-description">{description}</div>
        <a class="button" href="{etsy_url}" target="_blank" rel="noopener">Choose options on Etsy <span aria-hidden="true">↗</span></a>
        <p class="dialog-note">Secure ordering, variations and delivery are handled by Etsy.</p>
      </div>
    </article>
  </main>
  <footer>
    <a class="brand brand-footer" href="../../" aria-label="Lasair Studios home">
      <img class="brand-cow brand-cow-footer" src="../../assets/branding/cow-logo-transparent.png" alt="Lasair Studios Highland cow logo">
    </a>
    <p>Handmade objects for distinctive spaces.</p>
    <div><a href="https://www.etsy.com/uk/shop/LasairStudio" target="_blank" rel="noopener">Etsy</a><span>© {datetime.now(tz=UTC).year} Lasair Studios</span></div>
  </footer>
</body>
</html>
'''


def sync_product_pages(products: list[dict[str, object]]) -> None:
    PRODUCTS_DIR.mkdir(exist_ok=True)
    expected = {str(product["id"]) for product in products}
    for product in products:
        directory = PRODUCTS_DIR / str(product["id"])
        directory.mkdir(exist_ok=True)
        (directory / "index.html").write_text(render_product_page(product), encoding="utf-8")
    for existing in PRODUCTS_DIR.iterdir():
        if existing.is_dir() and existing.name.isdigit() and existing.name not in expected:
            shutil.rmtree(existing)


def render_sitemap(products: list[dict[str, object]]) -> str:
    dates = [str(product["updated"]) for product in products if product.get("updated")]
    homepage_lastmod = max(dates) if dates else None
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        "  <url>",
        f"    <loc>{SITE_ORIGIN}/</loc>",
    ]
    if homepage_lastmod:
        lines.append(f"    <lastmod>{homepage_lastmod}</lastmod>")
    lines.extend(["    <changefreq>weekly</changefreq>", "    <priority>1.0</priority>", "  </url>"])
    for product in products:
        product_id = html.escape(str(product["id"]))
        lines.extend(["  <url>", f"    <loc>{SITE_ORIGIN}/products/{product_id}/</loc>"])
        if product.get("updated"):
            lines.append(f"    <lastmod>{product['updated']}</lastmod>")
        lines.extend(["    <changefreq>weekly</changefreq>", "    <priority>0.8</priority>"])
        images = product.get("images", [])
        if images:
            lines.extend(
                [
                    "    <image:image>",
                    f"      <image:loc>{html.escape(str(images[0]))}</image:loc>",
                    f"      <image:title>{html.escape(str(product['name']))}</image:title>",
                    "    </image:image>",
                ]
            )
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def update_catalogue_asset_version(content: str) -> None:
    """Make browsers fetch each newly generated Etsy catalogue."""
    version = hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]
    index = INDEX_FILE.read_text(encoding="utf-8")
    updated, replacements = re.subn(
        r'etsy-products\.js(?:\?v=[^"\s]+)?',
        f"etsy-products.js?v={version}",
        index,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError("Could not update the Etsy catalogue asset version in index.html")
    INDEX_FILE.write_text(updated, encoding="utf-8")


def main() -> int:
    credentials = api_credentials()
    overlay, listings, images_by_id, new_listing_count = build_catalogue(credentials)
    products = seo_products(listings, images_by_id)
    content = (
        "// Generated by scripts/sync_etsy.py. Curated catalogue data remains in app.js.\n"
        f"window.etsyProducts = {json.dumps(overlay, ensure_ascii=False, indent=2)};\n"
    )
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    update_catalogue_asset_version(content)
    sync_product_pages(products)
    SITEMAP_FILE.write_text(render_sitemap(products), encoding="utf-8")
    active_count = sum(item.get("active") is True for item in overlay.values())
    inactive_count = sum(item.get("active") is False for item in overlay.values())
    print(
        f"Etsy sync prepared: {active_count} active curated listings, "
        f"{inactive_count} inactive curated listings, {len(products)} indexable product pages, "
        f"{new_listing_count} new listings awaiting homepage curation."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"Etsy sync stopped safely: {error}", file=sys.stderr)
        raise SystemExit(1)
