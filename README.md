# Lasair Studios website

A responsive catalogue site for Lasair Studios. Products are presented on the Lasair domain and purchases continue securely through the corresponding Etsy listing.

## Preview locally

Open `index.html` directly, or run any simple static web server from this directory.

## Structure

- `index.html` — page structure and content
- `styles.css` — responsive visual design
- `app.js` — curated catalogue data, filters and product detail gallery
- `etsy-products.js` — generated Etsy listing overlay
- `products/<listing-id>/index.html` — generated, crawlable product pages
- `sitemap.xml` — generated sitemap for the homepage and active Etsy products
- `robots.txt` — crawler permissions and sitemap discovery
- `scripts/sync_etsy.py` — read-only Etsy catalogue and SEO-page synchronisation
- `assets/branding` — supplied Lasair wordmark, handcrafted strapline and Highland cow artwork

## Etsy catalogue synchronisation

The `Sync Etsy catalogue` GitHub Actions workflow runs daily at 03:17 Europe/London and can also be run manually. It reads the `LASAIR_STUDIOS_ETSY` repository secret in `keystring:shared_secret` format, fetches public listing information from Etsy, updates `etsy-products.js`, generates one indexable page per active Etsy listing, refreshes `sitemap.xml`, and requests a GitHub Pages rebuild only when the generated data changes.

Etsy supplies listing titles, descriptions, prices, photographs and active status. Categories, tags, material summaries, specifications and exact listing links remain curated in `app.js`. New Etsy listings receive a product page and sitemap entry automatically; they still require curation before appearing in the homepage catalogue grid.

## GitKraken

This directory can be initialised as a Git repository and opened in GitKraken. No framework or build step is required, so it can be deployed to most static hosting providers.
