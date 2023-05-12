from earthdata_download import query
from earthdata_download import download


class EarthdataAPI:

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def query(
            self, short_name=None, version=None,
            start_date=None, end_date=None, extent=None,
            parse_entries=False):
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
        parse_entries : bool
            derive additional python types from entries
            like datetime timestamps and coverage polygons

        Returns
        -------
        list of dict
            entries
        """
        entries = query.get_entries(
            short_name=short_name, version=version,
            start_date=start_date, end_date=end_date,
            extent=extent, parse_entries=parse_entries)
        return entries

    @staticmethod
    def get_data_url(entry, *args, **kwargs):
        """Get data URL from entry

        Parameters
        ----------
        entry : dict
            entry from query
        *args, **kwargs : additional arguments
            passed to download.data_url_from_entry

        Returns
        -------
        str
            URL

        Note
        ----
        Override this if it does not work for you.
        """
        return download.data_url_from_entry(entry, *args, **kwargs)

    def get_data_urls(self, entries, *args, **kwargs):
        """Get data URLs from entries (just a multi-element version of get_data_url)

        Parameters
        ----------
        entries : list of dict
            entry dictionaries

        Returns
        -------
        list of str
            data URLs
        """
        return [self.get_data_url(e, *args, **kwargs) for e in entries]

    def download_single(self, product, download_dir='.',
                        local_filename=None, skip_existing=True, user_agent=None):
        """Download single data file

        Parameters
        ----------
        product : str or dict
            data URL or entry dictionary
        download_dir : str, optional
            directory to download to
        local_filename : str, optional
            direct path to target file
            alternative to download_dir
        skip_existing : bool
            consier existing files complete
            and do not redownload
        user_agent: str
            download using alternative user-agent in request.Session

        Returns
        -------
        str
            path to downloaded file
        """
        if isinstance(product, str):
            url = product
        else:
            url = self.get_data_url(product)
        lf = download.download_url(
            url,
            username=self.username, password=self.password,
            download_dir=download_dir,
            local_filename=local_filename,
            skip_existing=skip_existing,
            user_agent=user_agent)
        return lf

    def download(self, products, download_dir='.', skip_existing=True, user_agent=None):
        """Download multiple products

        Parameters
        ----------
        products : list of str or list of dict
            URLs or entries
        download_dir : str
            directory to download to
        skip_existing : bool
            consier existing files complete
            and do not redownload
        user_agent: str
            download using alternative user-agent in request.Session

        Returns
        -------
        list of str
            paths to downloaded files
        """
        local_filenames = []
        for product in products:
            lf = self.download_single(
                product, download_dir=download_dir, skip_existing=skip_existing, user_agent=user_agent)
            local_filenames.append(lf)
        return local_filenames
