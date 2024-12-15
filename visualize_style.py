import argparse
from pathlib import Path
from datasets import load_dataset
from PIL import Image
import torchvision.transforms as transforms
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Visualize and Save Specific Styles from WikiArt Dataset")
    parser.add_argument(
        '--styles',
        type=str,
        nargs='+',
        required=True,
        help='List of styles to visualize (e.g., "Realism", "Impressionism")'
    )
    parser.add_argument(
        '--num_images',
        type=int,
        default=10,
        help='Number of images to save per style'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='wikiart_styles',
        help='Directory to save the visualized images'
    )
    return parser.parse_args()

def save_images(dataset, styles, num_images, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Calculate 1% of the dataset
    sample_size = len(dataset) // 100
    print(f"Using {sample_size} images (1% of dataset)...")

    # Create a style-to-index mapping first using only 1% of data
    print("Creating style index...")
    style_indices = {}
    for idx in tqdm(range(sample_size)):
        item = dataset[idx]
        style = str(item['style']).lower()
        if style not in style_indices:
            style_indices[style] = []
        style_indices[style].append(idx)

    for style in styles:
        print(f"\nProcessing style: {style}")
        style_dir = output_path / style.replace(" ", "_")
        style_dir.mkdir(parents=True, exist_ok=True)

        # Get indices for current style
        style_idx = style_indices.get(style.lower(), [])
        
        # Check if there are enough images
        total_images = len(style_idx)
        if total_images == 0:
            print(f"No images found for style: {style}")
            continue

        images_to_save = min(num_images, total_images)
        print(f"Saving {images_to_save} images to {style_dir}...")

        # Use only the needed indices
        for i in tqdm(range(images_to_save), desc=f"Saving {style}"):
            idx = style_idx[i]
            image = dataset[idx]['image']
            image_filename = style_dir / f"{style.replace(' ', '_')}_{i+1}.jpg"
            image.save(image_filename)

        print(f"Saved {images_to_save} images for style: {style}")

def main():
    args = parse_arguments()
    
    # Load WikiArt dataset
    print("Loading WikiArt dataset...")
    dataset = load_dataset("huggan/wikiart", split='train')
    print("Dataset loaded successfully.\n")

    # Validate styles - Convert all styles to strings before applying lower()
    available_styles = sorted(list(set([str(style).lower() for style in dataset['style']])))

    selected_styles = [style.title() for style in args.styles]
    invalid_styles = [style for style in selected_styles if style.lower() not in available_styles]

    if invalid_styles:
        print(f"Error: The following styles are not available in the dataset: {', '.join(invalid_styles)}")
        print("Available styles are:")
        print(", ".join(sorted(set([str(style).title() for style in dataset['style']]))))
        return

    # Save images
    save_images(dataset, selected_styles, args.num_images, args.output_dir)
    print("Image saving completed.")

if __name__ == "__main__":
    main()