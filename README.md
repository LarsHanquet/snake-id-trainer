# Snake ID Trainer

An image-based snake identification game focused on observations from
Southeast Asia.

## Play online

Once GitHub Pages is enabled, the game will be available at:

`https://larshanquet.github.io/snake-id-trainer/`

## Run locally

Because this is a static site, it can be opened directly in a browser. For
the most reliable local behavior, serve the project directory with a small
HTTP server:

```powershell
py -m http.server 8000
```

Then open <http://localhost:8000>.

## Data and attribution

The bundled observations and image metadata were collected from
[iNaturalist](https://www.inaturalist.org/). Image attribution is included in
`assets/dataset_metadata.json` and is shown by the game where applicable.
Map tiles are provided by
[OpenStreetMap](https://www.openstreetmap.org/), and location lookups use
[Nominatim](https://nominatim.org/).

The `scrape.py` script can be used to regenerate the dataset. It requires the
Python packages used by the script (`requests` and `pyinaturalist`).

## GitHub Pages deployment

The workflow in `.github/workflows/pages.yml` publishes the repository root
to GitHub Pages whenever changes are pushed to `main`. In the repository
settings, set **Pages > Build and deployment > Source** to **GitHub Actions**.
