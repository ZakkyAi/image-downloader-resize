import os
from PIL import Image

def filter_and_resize_images(input_directory, output_directory, output_file, min_size=(100, 100), file_types=None):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    if file_types is None:
        file_types = {'.jpg', '.jpeg', '.png', '.gif'}

    with open(output_file, 'w') as f:
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)
            if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in file_types:
                try:
                    with Image.open(file_path) as img:
                        # Check the image size
                        if img.size[0] >= min_size[0] and img.size[1] >= min_size[1]:
                            # Resize the image to 128x128 pixels
                            resized_img = img.resize((128, 128))
                            # Save the resized image to the output directory
                            resized_path = os.path.join(output_directory, filename)
                            resized_img.save(resized_path)
                            f.write(resized_path + '\n')
                            print(f"Saved resized image path: {resized_path}")
                except Exception as e:
                    print(f"Could not process {file_path}: {e}")

# Usage
input_directory = r'hewan berkaki 4\four-legged animal'  # Fixed path
output_directory = 'resized_images'  # Directory to save resized images
output_file = 'filtered_image_paths.txt'  # File to save paths of resized images
filter_and_resize_images(input_directory, output_directory, output_file)
