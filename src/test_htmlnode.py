import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_value(self):
        node = LeafNode("p")
        self.assertIsNone(node.value)
    def test_tag(self):
        node = LeafNode(value="Hello, world!")
        self.assertIsNone(node.tag)
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child</span></div>")
    def test_to_html_with_2children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node,child_node2])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child</span><span>child2</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>")
    def test_to_html_with_2grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node = ParentNode("span", [grandchild_node,grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild2</b></span></div>")
    def test_to_html_with_noChildren(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(), 
            "<div></div>")
    def test_to_html_with_noneChild(self):
        parent_node = ParentNode("div",None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()