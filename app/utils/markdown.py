import markdown


def render_markdown(content: str) -> str:
    """
    Convert Markdown content to HTML.

    :param content: Markdown text
    :return: HTML string
    """
    return markdown.markdown(content)
