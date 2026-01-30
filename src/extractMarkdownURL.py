import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
def split_nodes_image(old_nodes):
    new_nodes = []
    for o in old_nodes:
        if o.text_type != TextType.PLAIN:
            new_nodes.append(o)
            continue
        img_ext = extract_markdown_images(o.text)
        if img_ext == None: #if no image markdown
            new_nodes.append(o)
            continue
        remaining_text = o.text #saving updated string for each loop
        for img in img_ext:
            before, after = remaining_text.split(f"![{img[0]}]({img[1]})",1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.PLAIN))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            remaining_text = after #updating string
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text,TextType.PLAIN))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for o in old_nodes:
        if o.text_type != TextType.PLAIN:
            new_nodes.append(o)
            continue
        link_ext = extract_markdown_links(o.text)
        if link_ext == None: #if no link markdown
            new_nodes.append(o)
            continue
        remaining_text = o.text #saving updated string for each loop
        for lnk in link_ext:
            before, after = remaining_text.split(f"[{lnk[0]}]({lnk[1]})",1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.PLAIN))
            new_nodes.append(TextNode(lnk[0], TextType.LINK, lnk[1]))
            remaining_text = after #updating string
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text,TextType.PLAIN))
    return new_nodes
