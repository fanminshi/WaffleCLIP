import argparse
from pathlib import Path
from datasets import load_dataset
from PIL import Image
import torchvision.transforms as transforms
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Visualize and Save Specific Genres from WikiArt Dataset")
    parser.add_argument(
        '--genres',
        type=str,
        nargs='+',
        required=True,
        help='List of genres to visualize (e.g., "Abstract", "Impressionism")'
    )
    parser.add_argument(
        '--num_images',
        type=int,
        default=10,
        help='Number of images to save per genre'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='wikiart_genres',
        help='Directory to save the visualized images'
    )
    return parser.parse_args()

def save_images(dataset, genres, num_images, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Calculate 1% of the dataset
    sample_size = len(dataset) // 100
    print(f"Using {sample_size} images (1% of dataset)...")

    # Create a genre-to-index mapping first using only 1% of data
    print("Creating genre index...")
    genre_indices = {}
    for idx in tqdm(range(sample_size)):
        item = dataset[idx]
        genre = str(item['genre']).lower()
        if genre not in genre_indices:
            genre_indices[genre] = []
        genre_indices[genre].append(idx)

    for genre in genres:
        print(f"\nProcessing genre: {genre}")
        genre_dir = output_path / genre.replace(" ", "_")
        genre_dir.mkdir(parents=True, exist_ok=True)

        # Get indices for current genre
        genre_idx = genre_indices.get(genre.lower(), [])
        
        # Check if there are enough images
        total_images = len(genre_idx)
        if total_images == 0:
            print(f"No images found for genre: {genre}")
            continue

        images_to_save = min(num_images, total_images)
        print(f"Saving {images_to_save} images to {genre_dir}...")

        # Use only the needed indices
        for i in tqdm(range(images_to_save), desc=f"Saving {genre}"):
            idx = genre_idx[i]
            image = dataset[idx]['image']
            image_filename = genre_dir / f"{genre.replace(' ', '_')}_{i+1}.jpg"
            image.save(image_filename)

        print(f"Saved {images_to_save} images for genre: {genre}")

def main():
    args = parse_arguments()
    
    # Load WikiArt dataset
    print("Loading WikiArt dataset...")
    dataset = load_dataset("huggan/wikiart", split='train')
    print("Dataset loaded successfully.\n")

    # Validate genres - Convert all genres to strings before applying lower()
    available_genres = sorted(list(set([str(genre).lower() for genre in dataset['genre']])))

    selected_genres = [genre.title() for genre in args.genres]
    invalid_genres = [genre for genre in selected_genres if genre.lower() not in available_genres]

    if invalid_genres:
        print(f"Error: The following genres are not available in the dataset: {', '.join(invalid_genres)}")
        print("Available genres are:")
        print(", ".join(sorted(set([str(genre).title() for genre in dataset['genre']]))))
        return

    # Save images
    save_images(dataset, selected_genres, args.num_images, args.output_dir)
    print("Image saving completed.")

if __name__ == "__main__":
    main()