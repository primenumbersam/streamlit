import os

# The directory containing the HTML files
target_dir = 'product-detail'

# Loop through all files in the target directory
for filename in os.listdir(target_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(target_dir, filename)
        
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace .png with .jpg
        new_content = content.replace('.png', '.jpg')
        
        # If the content has changed, write it back to the file
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated image sources in {filename}')

print("Done updating HTML files.")
