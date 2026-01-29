from textnode import TextNode, TextType

def main():
    test1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test1)

main()