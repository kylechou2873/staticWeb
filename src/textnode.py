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
def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block = ""
    for line in lines:
        if line.strip() == "": #end of a block
            if current_block.strip() != "":
                blocks.append(current_block.strip())
                current_block = ""
        else:
            if current_block == "": #part of current block
                current_block = line.strip()
            else:
                current_block += "\n" + line.strip()
    if current_block.strip() != "": #catch the last block
        blcoks.append(current_block.strip())
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"
def block_to_block_type(markdown: str) -> BlockType:
    if not markdown:
        return BlockType.PARAGRAPH
    
    block = markdown.strip("\n")

    #code block: ``` ```
    if block.startswith("```") and block.endswith("```") and len(block) >= 6:
        return BlockType.CODE

    #heading: 1-6#
    if block.startswith("#"):
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(block) and block[i] == " ":
            return BlockType.HEADING
    
    #quote: starts with ">"
    if block.startswith(">"):
        return BlockType.QUOTE

    #split into lines to check list blocks
    lines = [line for line in block.split("\n") if line.strip() != ""]

    if lines and all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    def parse_ordered_item(line: str) -> int | None:
        stripped = line.lstrip()
        i = 0
        while i < len(stripped) and stripped[i].isdigit():
            i += 1
        if i == 0 or i + 1 >= len(stripped):
            return None
        if stripped[i] ! = "." or stripped[i + 1] != " ":
            return None
        return int(stripped[:1])
    numbers = [parse_ordered_item(line) for line in lines]
    if all(n is not None for n in numbers):
        if numbers[0] == 1 and all(number[i] == i + 1 for i in range(len(numbers))):
            return BlockType.ORDERED_LIST
    
    if lines and all(is_ordered_item(line) for line in lines):
        return BlockType.ORDERED_LIST

    #Default
    return BlockType.PARAGRAPH