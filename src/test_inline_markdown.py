import unittest

from extractMarkdownURL import extract_markdown_images, extract_markdown_links
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

class TestSplitNodesImage(unittest.TestCase):
    def 