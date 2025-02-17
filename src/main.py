from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
from markdown_blocks import markdown_to_html_node
from rawmarkdown import extract_title
import os
import shutil

def copy_directory_recursive(source, destination):
    # Step 1: Remove all contents of the destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)  # Deletes everything inside the directory
    os.makedirs(destination)  # Recreate an empty destination directory

    # Step 2: Recursive function to copy files and directories
    def recursive_copy(src, dest):
        for item in os.listdir(src):  # Loop through items in the source directory
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(src_path):  # If it's a directory, recursively copy
                os.makedirs(dest_path, exist_ok=True)
                recursive_copy(src_path, dest_path)
            else:  # If it's a file, copy it
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} → {dest_path}")

    # Start copying
    recursive_copy(source, destination)
    print(f"\n✅ Successfully copied all contents from '{source}' to '{destination}'")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Copying items from {dir_path_content} to {dest_dir_path}")
    def recursive_copy_markdown(src, template, dest):
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            dest_item = dest_item.replace(".md",".html")
            #template_item = os.path.join(dest, item)

            if os.path.isdir(src_item):
                os.makedirs(dest_item, exist_ok=True)
                recursive_copy_markdown(src_item, template, dest_item)
            else:
                shutil.copy2(template, dest_item)
                print(f"Found {src_item} so copied blank {template} to {dest_item}")
                with open(src_item, "r") as file:
                    from_path_data = file.readlines()
                title = extract_title(from_path_data).strip()

                from_path_data = " ".join(from_path_data)
                markdown_from = markdown_to_html_node(from_path_data)
                markdown_from = markdown_from.to_html()

                with open(dest_item, "r") as file:
                    lines = file.readlines()
                with open(dest_item, "w") as file:
                    for line in lines:
                        if "{{ Title }}" in line:
                            file.write(line.replace("{{ Title }}",title))
                        elif "{{ Content }}" in line:
                            file.write(line.replace("{{ Content }}", markdown_from))
                        else:
                            file.write(line)

    recursive_copy_markdown(dir_path_content, template_path, dest_dir_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Page is being generated from {from_path} to the {dest_path} using themplate at {template_path}")
    shutil.copy2(template_path, dest_path)
    with open(from_path, "r") as file:
        from_path_data = file.readlines()
    title = extract_title(from_path_data).strip()

    from_path_data = " ".join(from_path_data)
    markdown_from = markdown_to_html_node(from_path_data)
    markdown_from = markdown_from.to_html()

    with open(dest_path, "r") as file:
        lines = file.readlines()
    with open(dest_path, "w") as file:
        for line in lines:
            if "{{ Title }}" in line:
                file.write(line.replace("{{ Title }}",title))
            elif "{{ Content }}" in line:
                file.write(line.replace("{{ Content }}", markdown_from))
            else:
                file.write(line)

copy_directory_recursive("static/", "public/")
#generate_page("content/index.md", "template.html", "public/index.html")
generate_pages_recursive("content/", "template.html", "public/")