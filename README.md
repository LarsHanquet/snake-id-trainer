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
Python packages used by the script (`requests` and `pyinaturalist`). It writes
to `assets/`, preserves downloaded observations, and saves metadata after each
observation so it can resume after an interruption.

## GitHub Pages deployment

The workflow in `.github/workflows/pages.yml` publishes the repository root
to GitHub Pages whenever changes are pushed to `main`. In the repository
settings, set **Pages > Build and deployment > Source** to **GitHub Actions**.

## Rebuilding and pushing the full dataset

Run the scraper from the repository root:

```powershell
py scrape.py
```

The scraper currently targets up to 5,000 observations. It may produce many
thousands of image files. To commit them in batches of 250 and push each
batch:

```powershell
.\push-dataset-batches.ps1 -BatchSize 250 -Push
```

Review the staged files first by omitting `-Push`. GitHub's repository and
Pages limits still apply to the completed repository; batching changes transfer
size and recoverability, not the final storage used.
