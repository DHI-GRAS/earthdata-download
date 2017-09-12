from . import query
from . import download


class NoDataError(Exception):
    pass


class EarthdataAPI:

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def find_data(
            self, short_name='', version='',
            start_date=None, end_date=None, extent={}, linkno=0):
        """Find data for query

        Parameters
        ----------
        short_name : str
            product short name
        version : str
            product version (e.g. '005', leading zeros matter!)
        date_range : (datetime.datetime, datetime.datetime)
            date range
            at least one must be specified
        extent : dict
            extent dictionary
            must have entries xmin, xmax, ymin, ymax
        linkno : int
            number of link to get
            different products have different links
            e.g. opendap etc.
            0 is usually a good download link

        Returns
        -------
        urls : list of str
            data download URLs
        """
        data_urls = query.find_data(
                short_name=short_name, version=version,
                start_date=start_date, end_date=end_date,
                extent=extent, linkno=linkno)
        if not data_urls:
            raise NoDataError('No data found for this query.')
        return data_urls

    def download_single(self, url, download_dir='.', local_filename=None):
        """Download single data file from url"""
        lf = download.download_data(url,
                self.username, self.password,
                download_dir=download_dir,
                local_filename=local_filename)
        return lf

    def download_all(self, data_urls, download_dir='.'):
        """Download all data in (self.)data_urls"""
        local_filenames = []
        for url in data_urls:
            lf = self.download_single(url, download_dir=download_dir)
            local_filenames.append(lf)
        return local_filenames
