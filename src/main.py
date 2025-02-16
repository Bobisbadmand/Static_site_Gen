from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

def main():
    print(TextNode("Hello", TextType.BOLD))

main()