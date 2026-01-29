import unittest

from htmlnode import HTMLNode 


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is the paragraph", ["a", "b", "c"], {"key":"1","key2":"2"})
        node2 = HTMLNode("p", "this is the paragraph", ["a", "b", "c"], {"key":"1","key2":"2"})
        self.assertEqual(node, node2)
    def test_children(self):
        node = HTMLNode("p", "this is the paragraph")
        self.assertIsNone(node.children)
    def test_props(self):
        node = HTMLNode("p", "this is the paragraph", children = ["a", "b", "c"])
        self.assertIsNone(node.props)
    def test_noteq(self):
        node = HTMLNode("p", "this is the paragraph", ["a", "b", "c"], {"key":"1","key2":"2"})
        node2 = HTMLNode("a", "this is the paragraph", ["a", "b", "c"], {"key":"1","key2":"2"})
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()