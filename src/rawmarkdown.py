from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
            continue
        
        current_node_list = []
        current_node = old.text.split(delimiter)
        if len(current_node) % 2 == 0:
            raise ValueError("Invalid markdown syntax was used cannot convert from raw markdown")
        
        for current in range(len(current_node)):
            if current_node[current] == "":
                continue
            if current % 2 == 0:
                current_node_list.append(TextNode(current_node[current], TextType.TEXT))
            else:
                current_node_list.append(TextNode(current_node[current], text_type))

        new_nodes.extend(current_node_list)

    return new_nodes


def extract_markdown_images(text):
#    extracted = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    extracted = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return extracted

def extract_markdown_links(text):
    extracted = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return extracted  

def split_nodes_image(old_nodes):
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
            continue

        original_text = old.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old)
            continue

        for image in images:
            section = original_text.split(f"![{image[0]}]({image[1]})",1)
            if len(section) != 2:
                raise ValueError("invalid markdown, image not available")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
            
            original_text = section[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

        return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
            continue

        original_text = old.text
        links = extract_markdown_links(original_text)
        for link in links:
            section = original_text.split(f"[{link[0]}]({link[1]})")
            if len(section) != 2:
                raise ValueError("invalid markdown, no link found")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT ))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            original_text = section[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

        return new_nodes

