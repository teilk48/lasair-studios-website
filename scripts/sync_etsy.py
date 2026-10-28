#!/usr/bin/env python3
"""Synchronise public Etsy listing data into the Lasair catalogue overlay."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.etsy.com/v3/application"
SHOP_NAME = "LasairStudio"
ROOT = Path(__file__).resolve().parents[1]
APP_FILE = ROOT / "app.js"
OUTPUT_FILE = ROOT / "etsy-products.js"


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


def build_overlay(credentials: str) -> tuple[dict[str, dict[str, object]], int]:
    ids = curated_ids()
    shop_id = find_shop_id(credentials)
    listings = active_listings(shop_id, credentials)
    by_id = {str(listing["listing_id"]): listing for listing in listings}
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
        images = listing_images(listing_id, credentials)
        if images:
            updated["images"] = images
        if not updated["name"] or not updated["description"]:
            raise RuntimeError(f"Listing {listing_id} is missing a title or description")
        overlay[listing_id] = updated

    new_listing_count = len(set(by_id) - set(ids))
    return overlay, new_listing_count


def main() -> int:
    credentials = api_credentials()
    overlay, new_listing_count = build_overlay(credentials)
    content = (
        "// Generated by scripts/sync_etsy.py. Curated catalogue data remains in app.js.\n"
        f"window.etsyProducts = {json.dumps(overlay, ensure_ascii=False, indent=2)};\n"
    )
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    active_count = sum(item.get("active") is True for item in overlay.values())
    inactive_count = sum(item.get("active") is False for item in overlay.values())
    print(
        f"Etsy sync prepared: {active_count} active curated listings, "
        f"{inactive_count} inactive curated listings, {new_listing_count} new listings awaiting curation."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"Etsy sync stopped safely: {error}", file=sys.stderr)
        raise SystemExit(1)
