class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k,v in self.props.items())
    def __eq__(self,other):
        if not isinstance(other, HTMLNode):
            return False
        return(
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self,tag=None,value=None,props=None):
        super().__init__(tag, value)
        self.props = props or {}
    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        props_list = "".join(f' {k}="{v}"' for k,v in self.props.items())
        return (f"<{self.tag}{props_list}>{self.value}</{self.tag}>")
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,value=None,children=children,props=props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        child_list = "".join([c.to_html() for c in self.children])
        return (f"<{self.tag}>{child_list}</{self.tag}>")
    
