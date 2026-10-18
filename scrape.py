import json
import os
import re
import time
import requests
from pyinaturalist import get_observations

# --- Configuration ---
TAXON_ID = 85553  # Suborder Serpentes (Snakes)
# Place IDs: 6967 (Thailand), 6992 (Vietnam), 7001 (Laos)
PLACE_IDS = [6967, 6992, 7001]

QUALITY_GRADE = "research"  # Guarantees community consensus on species
PER_PAGE = 30
MAX_OBSERVATIONS = 5000  # Adjust as needed for your dataset size
OUTPUT_DIR = "snake_game_dataset"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)


def sanitize_filename(name):
    """Cleans strings to ensure valid and consistent file system names."""
    if not name:
        return "unknown"
    # Remove characters that are unsafe for filenames and replace spaces with underscores
    clean = re.sub(r"[^\w\s-]", "", str(name)).strip().replace(" ", "_")
    return clean.lower()


def download_image(url, save_path):
    """Downloads an image file with standard user-agent header."""
    headers = {"User-Agent": "SnakeIDGameTrainer/1.0 (educational project)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False


def extract_snake_game_data():
    dataset = []
    page = 1
    total_fetched = 0

    print("Fetching snake observations for SE Asia (Vietnam, Laos, Thailand)...")

    while total_fetched < MAX_OBSERVATIONS:
        # Query API filtering by snake Taxon ID and target Place IDs
        response = get_observations(
            taxon_id=TAXON_ID,
            place_id=PLACE_IDS,
            quality_grade=QUALITY_GRADE,
            photos=True,  # Restrict to observations with photos
            per_page=PER_PAGE,
            page=page,
            locale="en",
        )

        results = response.get("results", [])
        if not results:
            print("No more results returned from API.")
            break

        for obs in results:
            if total_fetched >= MAX_OBSERVATIONS:
                break

            # Extract community taxon (species identity)
            taxon = obs.get("taxon")
            if not taxon or taxon.get("rank") != "species":
                continue  # Ensure observation is identified to species level

            obs_id = obs["id"]
            species_id = taxon["id"]
            scientific_name = taxon.get("name")
            common_name = taxon.get("preferred_common_name", scientific_name)

            # Get place info where observation occurred
            place_guess = obs.get("place_guess", "SE Asia")

            # Prepare sanitized elements for filename formatting
            clean_loc = sanitize_filename(place_guess)
            clean_spec = sanitize_filename(scientific_name)

            # Collect and download images
            photos = obs.get("photos", [])
            downloaded_photos = []

            for idx, p in enumerate(photos):
                # Replace 'square' thumbnail with 'medium' (approx 500px) or 'large' (1024px)
                photo_url = p.get("url", "").replace("square", "medium")
                if not photo_url:
                    continue

                # Updated filename format: location_species_obsID_pIndex.jpg
                filename = f"{clean_loc}_{clean_spec}_{obs_id}_p{idx}.jpg"
                local_path = os.path.join(IMAGES_DIR, filename)

                if download_image(photo_url, local_path):
                    downloaded_photos.append(
                        {
                            "file_name": filename,
                            "original_url": photo_url,
                            "attribution": p.get("attribution", ""),
                        }
                    )

            if downloaded_photos:
                dataset.append(
                    {
                        "observation_id": obs_id,
                        "species_id": species_id,
                        "scientific_name": scientific_name,
                        "common_name": common_name,
                        "location_name": place_guess,
                        "images": downloaded_photos,
                    }
                )
                total_fetched += 1
                print(
                    f"[{total_fetched}/{MAX_OBSERVATIONS}] Saved image: {filename}"
                )

        page += 1
        time.sleep(1)  # Respect API rate limits (1 req/sec)

    # Export dataset index JSON
    meta_path = os.path.join(OUTPUT_DIR, "dataset_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\nExtraction complete! Dataset saved in '{OUTPUT_DIR}'")


if __name__ == "__main__":
    extract_snake_game_data()