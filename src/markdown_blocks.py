import re

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
            print(f"printing ordered list: {orderedlist}")
            orderedlist +=1
    if quotecounter == len(quoteblock):
        return block_type_quote
    if unorderedlist == len(quoteblock):
        return block_type_ulist
    if orderedlist == len(quoteblock):
       return block_type_olist
    
    return block_type_paragraph
    

    