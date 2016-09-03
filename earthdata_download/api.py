from . import query
from . import download

class EarthdataAPI:

    def __init__(self, username, password):
        self.data_urls = []
        self.username = username
        self.password = password

    def find_data(self, short_name='', version='', start_date=None, end_date=None, extent={}):
        """Find data for query"""
        data_urls = query.find_data(
                short_name=short_name, version=version,
                start_date=start_date, end_date=end_date,
                extent=extent)
        if not data_urls:
            raise RuntimeError('No data found for this ')
        self.data_urls += data_urls
        return data_urls

    def download_single(self, url, download_dir='.', local_filename=None,
            username=None, password=None):
        """Download single data file from url"""
        username = username or self.username
        password = password or self.password
        lf = download.download_data(url,
                username, password,
                download_dir=download_dir,
                local_filename=local_filename)
        return lf

    def download_all(self, download_dir='.', username=None, password=None):
        """Download all data in data_urls"""
        local_filenames = []
        for url in self.data_urls:
            lf = self.download_single(url,
                    username, password,
                    download_dir=download_dir)
            local_filenames.apend(lf)
        return local_filenames
