# Lasair Studios website

A responsive catalogue site for Lasair Studios. Products are presented on the Lasair domain and purchases continue securely through the corresponding Etsy listing.

## Preview locally

Open `index.html` directly, or run any simple static web server from this directory.

## Structure

- `index.html` — page structure and content
- `styles.css` — responsive visual design
- `app.js` — curated catalogue data, filters and product detail gallery
- `etsy-products.js` — generated Etsy listing overlay
- `scripts/sync_etsy.py` — read-only Etsy catalogue synchronisation
- `assets/branding` — supplied Lasair wordmark, handcrafted strapline and Highland cow artwork

## Etsy catalogue synchronisation

The `Sync Etsy catalogue` GitHub Actions workflow runs daily at 03:17 Europe/London and can also be run manually. It reads the `LASAIR_STUDIOS_ETSY` repository secret in `keystring:shared_secret` format, fetches public listing information from Etsy, updates `etsy-products.js`, and requests a GitHub Pages rebuild only when the generated data changes.

Etsy supplies listing titles, descriptions, prices, photographs and active status. Categories, tags, material summaries, specifications and exact listing links remain curated in `app.js`. New Etsy listings are reported by the workflow and require curation before appearing on the website.

## GitKraken

This directory can be initialised as a Git repository and opened in GitKraken. No framework or build step is required, so it can be deployed to most static hosting providers.
