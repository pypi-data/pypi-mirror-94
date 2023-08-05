def create_file_public_url(url, filename):
    if url.endswith('/'):
        url = url[:-1]
    return '/'.join(url, filename)
