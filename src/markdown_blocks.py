import re
from textnode import TextNode, HTMLNode, text_node_to_html_node, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from rawmarkdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
#    splitmarkdown = markdown.split("\n\n")
#    splitmarkdown = [item.strip() for item in splitmarkdown if item != ""]

    splitmarkdown = re.split(r"(\n)\s", markdown)
    splitmarkdown = [item for item in splitmarkdown if item != '\n']
    splitmarkdown = [item.strip() for item in splitmarkdown if item != ""]
    return splitmarkdown


def block_to_block_type(block):
    for b in range(len(block)):
        if block[b:b+2] == "# " and block[b+2] != "":
            return block_type_heading
        if block[b:b+4] == "```" and block[-3:] == "```":
            return block_type_code
        
    quoteblock = block.split("\n")
    quotecounter = 0
    unorderedlist = 0
    orderedlist = 0
    for line in quoteblock:
        if line[0] == ">":
            quotecounter+=1
        elif line[0:2] == "* " or line[0:2] == "- ":
            unorderedlist +=1
        elif line[0:3] == f"{orderedlist+1}. ":
            #print(f"printing ordered list: {orderedlist}")
            orderedlist +=1
    if quotecounter == len(quoteblock):
        return block_type_quote
    if unorderedlist == len(quoteblock):
        return block_type_ulist
    if orderedlist == len(quoteblock):
       return block_type_olist
    
    return block_type_paragraph
    
def markdown_to_html_node(markdown):
    markdowns = markdown_to_blocks(markdown)
    children = []
    for mark in markdowns:
        html_mode = block_to_html(mark)
        children.append(html_mode)
    return ParentNode("div",children,None)


def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    block_split = block.split("\n")
    paragraph = " ".join(block_split)
    child = text_to_children(paragraph)
    return ParentNode("p",child)

def heading_to_html_node(block):
    levelheader = 0
    for b in block:
        if b == "#":
            levelheader += 1
        else:
            break
    
    if levelheader+1 >= len(block):
        raise ValueError(f"inproper header level {levelheader}")
    non_header_text = block[levelheader+1:]
    child = text_to_children(non_header_text)
    return ParentNode(f"h{levelheader}", child)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    non_code_text = block[4:-3]
    child = text_to_children(non_code_text)
    code = ParentNode("code", child)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    item_list = block.split("\n")
    html_items = []
    for item in item_list:
        text = item[3:]
        child = text_to_children(text)
        html_items.append(ParentNode("li", child))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    item_list = block.split("\n")
    html_items = []
    for item in item_list:
        text = item[2:]
        child = text_to_children(text)
        html_items.append(ParentNode("li",child))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)