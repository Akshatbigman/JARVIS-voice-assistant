import webbrowser


def website_opener(domain):
    """
    This will open website according to domain
    :param domain: any domain, example "youtube.com"
    :return: True if success, False if fail
    """
    try:
        url = 'https://www.' + domain + '.com'
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False
