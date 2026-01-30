from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self,other):
        return self.text==other.text and self.text_type==other.text_type and self.url == other.url
    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid TextType: {text_node.text_type}")
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for o in old_nodes:
        if o.text_type != TextType.PLAIN:
            new_nodes.append(o)
            continue
        splits = o.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise Exception("inline markdown mismatch")
        else:
            node_to_add = []
            for s in range(len(splits)):
                if splits[s] == "":
                    continue
                if s % 2 == 0:
                    node_to_add.append(TextNode(splits[s],TextType.PLAIN))
                else:
                    node_to_add.append(TextNode(splits[s],text_type))
            new_nodes.extend(node_to_add)
    return new_nodes
