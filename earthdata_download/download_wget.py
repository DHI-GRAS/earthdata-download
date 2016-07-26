import os
import posixpath
import subprocess
import re
import logging

wget_exe = os.path.join(os.path.dirname(__file__), 'wget64.exe')

def download_data(url, username, password, download_dir='.', local_filename='',
        logger=None):
    """Download a url with login using wget"""

    if logger is None:
        logger = logging

    # generate local file name
    if not local_filename:
        local_filename = os.path.join(download_dir, posixpath.basename(url))

    # put together command
    cmd = [wget_exe, '-L', '-c', '-N']
    cmd += ['--user='+username, '--password='+password]
    cmd += ['-O', local_filename]
    cmd += [url]

    logger.debug('Download command is \'{}\'.'.format(' '.join(cmd)))

    # execute command
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

    return local_filename
