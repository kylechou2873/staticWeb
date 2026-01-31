import unittest

from textnode import TextNode, TextType, text_node_to_html_node, markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
    def test_noteq(self):
        node = TextNode("Test", TextType.ITALIC)
        node2 = TextNode("Test", TextType.BOLD)
        self.assertNotEqual(node, node2)
class testTextNode_to_htmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "test.link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href":"test.link"})

class testMarkdown2Blocks(unittest.TestCase):
    def test_markdown(self):
        md ="""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



if __name__ == "__main__":
    unittest.main()