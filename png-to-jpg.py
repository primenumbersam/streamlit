from PIL import Image
import os

# Source directory
source_dir = 'assets'

# Loop through files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith('.png'):
        # Open the image
        img_path = os.path.join(source_dir, filename)
        img = Image.open(img_path)

        # Create the new filename
        new_filename = os.path.splitext(filename)[0] + '.jpg'
        new_img_path = os.path.join(source_dir, new_filename)

        # Convert to RGB if it has an alpha channel
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Save as JPG
        img.save(new_img_path, 'jpeg')
        print(f'Converted {filename} to {new_filename} and replaced it.')

        # Remove the original PNG file
        os.remove(img_path)
