import unittest
from rawmarkdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_title
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    
class TestImageExtract(unittest.TestCase):
    def test_image_extract(self):
        text = """This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"""
        results = extract_markdown_images(text)
        self.assertEqual(str(results),"""[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]""")
    
    def test_basic_case(self):
        text = "![alt text](https://example.com/image.jpg)"
        expected = [('alt text', 'https://example.com/image.jpg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_normal_case(self):
        text = "This is an image: ![dog](https://dogs.com/dog.png)"
        expected = [('dog', 'https://dogs.com/dog.png')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "Multiple images ![cat](https://cats.com/cat.jpg) and ![bird](https://birds.com/bird.png)"
        expected = [('cat', 'https://cats.com/cat.jpg'), ('bird', 'https://birds.com/bird.png')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_alt_text(self):
        text = "No alt text ![](https://example.com/blank.jpg)"
        expected = [('', 'https://example.com/blank.jpg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_spaces_in_alt_text(self):
        text = "Spaces in alt text ![a cute cat](https://example.com/cat.jpg)"
        expected = [('a cute cat', 'https://example.com/cat.jpg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_nested_brackets_in_alt(self):
        text = "Nested brackets ![a nested alt](https://example.com/nested.jpg)"
        expected = [('a nested alt', 'https://example.com/nested.jpg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_parentheses_in_url(self):
        text = "Unescaped parentheses in URL ![alt](https://example.com/path1.jpg)"
        expected = [('alt', 'https://example.com/path1.jpg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_missing_exclamation_mark(self):
        text = "[alt text](https://example.com/not-an-image.jpg)"  # Shouldn't be matched
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images_in_text(self):
        text = "Random text without markdown images"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_extract(self):
        text = """This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"""
        results = extract_markdown_links(text)
        self.assertEqual(str(results),"""[('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]""")

    def test_basic_case(self):
        text = "[Google](https://www.google.com)"
        expected = [('Google', 'https://www.google.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_spaces_in_link_text(self):
        text = "Click here for [OpenAI](https://www.openai.com)"
        expected = [('OpenAI', 'https://www.openai.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[Google](https://www.google.com) and [GitHub](https://www.github.com)"
        expected = [('Google', 'https://www.google.com'), ('GitHub', 'https://www.github.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_link_text(self):
        text = "[empty text](https://example.com)"
        expected = [('empty text', 'https://example.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_special_characters(self):
        text = "[This is a test](https://example.com/test?query=123&other=test)"
        expected = [('This is a test', 'https://example.com/test?query=123&other=test')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links_in_text(self):
        text = "This is just some random text with no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_missing_url(self):
        text = "[missing URL]()"
        expected = [('missing URL', '')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_missing_link_text(self):
        text = "[](https://example.com)"
        expected = [('', 'https://example.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_invalid_markdown_format(self):
        text = "[not a valid link](https://example.com"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_parentheses_in_url(self):
        text = "[link with parens](https://example.com/test1.jpg)"
        expected = [('link with parens', 'https://example.com/test1.jpg')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_nested_brackets_in_link_text(self):
        text = "[a [nested] link](https://example.com)"
        expected = [('a [nested] link', 'https://example.com')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

class TestSplitNodes(unittest.TestCase):        
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    
class TestTextNodeJoin(unittest.TestCase):
    def test_textnodes(self):
        text = """This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        result = (text_to_textnodes(text))

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

class TestExtractTitle(unittest.TestCase):
    def test_extracttitle(self):
        text = "# this is a title"
        result = extract_title([text])
        self.assertEqual(result, "this is a title")


    


if __name__ == "__main__":
    unittest.main()
