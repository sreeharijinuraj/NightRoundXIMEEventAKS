import re
import os

files_to_update = [
    'pricing.html',
    'about.html',
    'product.html',
    'login.html',
    'signup.html',
    'contactus.html'
]

def get_block(text, tag):
    pattern = rf'<{tag}[^>]*>.*?</{tag}>'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def update_files():
    # Read source file
    src_file = r'd:\NightRound - TeamAKS\index.html'
    with open(src_file, 'r', encoding='utf-8') as f:
        src_content = f.read()

    header_block = get_block(src_content, 'header')
    footer_block = get_block(src_content, 'footer')

    if not header_block or not footer_block:
        print("Error: Could not extract header or footer from index.html")
        return

    base_dir = r'd:\NightRound - TeamAKS'
        
    for file_name in files_to_update:
        file_path = os.path.join(base_dir, file_name)
        if not os.path.exists(file_path):
            print(f"Skipping {file_name} - not found")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace header
        header_pattern = r'<header[^>]*>.*?</header>'
        content = re.sub(header_pattern, lambda m: header_block, content, flags=re.DOTALL | re.IGNORECASE)
        
        # Replace footer
        footer_pattern = r'<footer[^>]*>.*?</footer>'
        content = re.sub(footer_pattern, lambda m: footer_block, content, flags=re.DOTALL | re.IGNORECASE)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated {file_name}")

if __name__ == "__main__":
    update_files()
