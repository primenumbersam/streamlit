import os
import re

def update_index_html():
    target_dir = 'product-detail'
    index_file = 'index.html'
    
    # 1. Get all .html files except index.html
    files = [f for f in os.listdir(target_dir) if f.endswith('.html') and f != 'index.html']
    files.sort()
    
    # Create the JS-style array string
    files_js_array = "const htmlFiles = [\n                " + ",\n                ".join([f"'{f}'" for f in files]) + "\n            ];"
    
    if not os.path.exists(index_file):
        print(f"Error: {index_file} not found.")
        return

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. Use Regex to find the htmlFiles array and replace it
    pattern = r"const htmlFiles = \[[\s\S]*?\];"
    new_content = re.sub(pattern, files_js_array, content)

    if new_content != content:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated {index_file} with {len(files)} projects.")
    else:
        print("No changes detected in project list.")

if __name__ == "__main__":
    update_index_html()