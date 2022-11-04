def check_url(url):
    if url[0:8] != 'https://':
        new_url = 'https://' + url
        return new_url
    elif url[0:8] == 'https://':
        return url