from requests import get


def get_page(url):
    """
    Get the text of a page from a url
    :param url: url of page
    :return: text from the page
    """
    return get(url).text
