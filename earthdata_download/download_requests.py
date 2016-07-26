import os
import posixpath
import requests
from lxml import html

earthdata_login_url = 'https://urs.earthdata.nasa.gov/'


def _download_file(url, local_filename='', local_dir='', **kwargs):
    """Download a large file using requests"""
    if not local_filename:
        local_filename = os.path.join(local_dir, posixpath.basename(url))
    # Note the stream=True parameter
    r = requests.get(url, stream=True, **kwargs)
    _download_file_response(r, local_filename)
    return local_filename


def _download_file_response(r, local_filename):
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def _get_authenticity_token(r):
    tree = html.fromstring(r.text)
    authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]
    return authenticity_token


def download_data(data_urls, auth, download_dir=''):
    """Download data files from EarthData ECHO REST"""

    # define payload (must match form field IDs from website HTML)
    earthdata_login_payload = {
            'username': auth[0],
            'password': auth[1]}

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Host': 'urs.earthdata.nasa.gov',
            'Referer': 'https://urs.earthdata.nasa.gov'}

    downloaded_files = []
    for url in data_urls:

        with requests.Session() as s:

            # get authenticity token
            r_login = s.get(earthdata_login_url)
            earthdata_login_payload['authenticity_token'] = \
                _get_authenticity_token(r_login)

            print(earthdata_login_payload)

            # log in
            p = s.post(earthdata_login_url, allow_redirects=True,
                    data=earthdata_login_payload,
                    headers=headers)
            if p.status_code in [404, 401]:
                raise RuntimeError('Login failed (status code {}).\n\n{}'
                        ''.format(p.status_code, p.text))
            print(p.text)

            # get data file
            r = s.get(url, stream=True)
            local_filename = os.path.join(download_dir, posixpath.basename(url))
            _download_file_response(r, local_filename=local_filename)

        # check if file is empty
        if os.stat(local_filename).st_size < 100:
            os.remove(local_filename)
            raise ValueError('Download of url \'{}\' failed.'.format(url))

        downloaded_files.append(local_filename)

    return downloaded_files
