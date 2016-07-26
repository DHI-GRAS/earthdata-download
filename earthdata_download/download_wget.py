import os
import subprocess
import re
import logging

wget_exe = os.path.join(os.path.dirname(__file__), 'wget64.exe')

def download_data(url, download_dir='.', username='Jessen5678', password='Drought2016', logger=None):
    """Download a url with login using wget"""

    if logger is None:
        logger = logging.getLogger('wget')
        logger.setLevel(logging.DEBUG)

    cmd = [wget_exe, '-L', '--user='+username, '--password='+password, '-P', download_dir, url]

    logger.debug('Download command is \'{}\'.'.format(' '.join(cmd)))

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    n = 0
    last_percent = ''
    for line in iter(proc.stdout.readline, ''):
        n += 1
        if n <= 10:
            # print the first 10 lines
            logger.info(line.rstrip())
        elif '%' in line:
            # get and log status
            try:
                percent = re.search('(\d{1,3}\%)', line).group(0)
                if percent != last_percent:
                    logger.info(percent)
                    last_percent = percent
            except IndexError:
                pass
        if 'ERROR' in line:
            # fail on errors
            raise RuntimeError('Download of {} failed: {}'.format(url, line.rstrip()))
