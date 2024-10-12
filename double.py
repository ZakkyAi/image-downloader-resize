import os
import hashlib
from PIL import Image

def hash_image(image_path):
    """Generate a hash for the image file."""
    with Image.open(image_path) as img:
        img = img.resize((256, 256)).convert('RGB')  # Resize for faster comparison
        image_bytes = img.tobytes()
        return hashlib.md5(image_bytes).hexdigest()

def find_and_remove_duplicates(input_directory, output_directory):
    """Find and remove duplicate images based on content."""
    hashes = {}
    duplicates = []

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and file_path.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            image_hash = hash_image(file_path)

            if image_hash in hashes:
                print(f"Duplicate found: {file_path} (duplicate of {hashes[image_hash]})")
                duplicates.append(file_path)  # Mark the duplicate for deletion
            else:
                # If it's not a duplicate, copy it to the output directory
                hashes[image_hash] = file_path
                output_path = os.path.join(output_directory, filename)
                Image.open(file_path).save(output_path)
                print(f"Saved non-duplicate image: {output_path}")

    # Delete duplicate images
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Deleted: {duplicate}")

# Usage
input_directory = r'poltek\politeknik negeri sriwijaya'  # Your input folder
output_directory = 'check double image poltek'  # Your output folder for non-duplicates

# Call the function to find and remove duplicates
find_and_remove_duplicates(input_directory, output_directory)
