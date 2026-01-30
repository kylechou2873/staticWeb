import unittest

from extractMarkdownURL import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType, split_nodes_delimiter

class testSplitNodeDelimiter(unittest.TestCase):
    def testCODEtype(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node],"`",TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN)]) 
    def testBOLDtype(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node],"**",TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.PLAIN)]) 
    def testITALICtype(self):
        node = TextNode("This is text with a _ital block_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node],"_",TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [TextNode("This is text with a ", TextType.PLAIN),
            TextNode("ital block", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN)]) 

class TestExtractMarkImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
class TestExtractMarkLink(unittest.TestCase):
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.links.com)"
        )
        self.assertListEqual([("link", "https://www.links.com")], matches)

class TestSplitNodesLinkAndImag(unittest.TestCase):
    def test_SplitNodeImage_w2Links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestTextToNode(unittest.TestCase):
    def test_text_to_TextNodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        re_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            re_nodes,
        )