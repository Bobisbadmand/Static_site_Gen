from textnode import TextType, TextNode

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

    raise ValueError("Invalid markdown syntax was used cannot convert from raw markdown")