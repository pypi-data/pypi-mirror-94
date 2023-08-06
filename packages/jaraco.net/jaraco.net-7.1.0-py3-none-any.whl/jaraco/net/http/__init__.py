"""
HTTP routines
"""

import logging
import os
import re
import datetime
import argparse
import cgi
import urllib
import http.client as http_client

import jaraco.text
import jaraco.path

log = logging.getLogger(__name__)


class Query(dict):
    """HTTP Query takes as an argument an HTTP query request
    (from the url after ?) or a URL and maps all of the query pairs
    in itself as a dictionary.
    >>> Query('a=b&c=3&4=20') == {'a':'b', 'c':'3', '4':'20'}
    True
    >>> Query('http://www.jaraco.com/?test=30') == {'test':'30'}
    True
    >>> Query('http://www.jaraco.com/') == {}
    True
    >>> Query('') == {}
    True
    """

    def __init__(self, query):
        query = Query.__QueryFromURL__(query) or query
        if not re.match(r'(\w+=\w+(&\w+=\w+)*)*$', query):
            query = ()
        if isinstance(query, str):
            items = query.split('&')
            # remove any empty values
            items = filter(None, items)
            itemPairs = map(jaraco.text.Splitter('='), items)

            def unquoteSequence(seq):
                return map(urllib.parse.unquote, seq)

            query = map(unquoteSequence, itemPairs)
        if not isinstance(query, dict):
            query = dict(query)
        if not isinstance(query, dict):
            msg = "Can't construct a %s from %s"
            raise ValueError(msg % (self.__class__, query))
        self.update(query)

    def __repr__(self):
        return urllib.parse.urlencode(self)

    @staticmethod
    def __QueryFromURL__(url):
        "Return the query portion of a URL"
        return urllib.parse.urlparse(url).query


def get_content_disposition_filename(url):
    """
    Get the content disposition filename from a URL.
    Returns None if no such disposition can be found.

    If `url` is already a response object, it will use its headers.
    Otherwise, urllib.request is used to retrieve the headers.

    >>> url = 'http://www.voidspace.org.uk/cgi-bin'
    >>> url += '/voidspace/downman.py?file=pythonutils-0.3.0.zip'
    >>> get_content_disposition_filename(url) in (None, 'pythonutils-0.3.0.zip')
    True

    >>> url = 'http://www.example.com/invalid_url'
    >>> get_content_disposition_filename(url) is None
    True

    >>> url = 'http://www.google.com/'
    >>> get_content_disposition_filename(url) is None
    True

    """

    res = url
    if not getattr(res, 'headers', None):
        req = urllib.request.Request(url, method='HEAD')
        try:
            res = urllib.request.urlopen(req)
        except urllib.error.URLError:
            return
    header = res.headers.get('content-disposition', '')
    value, params = cgi.parse_header(header)
    return params.get('filename')


def get_url_filename(url):
    return os.path.basename(urllib.parse.urlparse(url).path)


def get_url(url, dest=None, replace_newer=False, touch_older=True):
    src = urllib.request.urlopen(url)
    log.debug(src.headers)
    if 'last-modified' in src.headers:
        mod_time = datetime.datetime.strptime(
            src.headers['last-modified'], '%a, %d %b %Y %H:%M:%S %Z'
        )
    else:
        mod_time = None
    content_length = int(src.headers['content-length'])
    fname = (
        dest
        or get_content_disposition_filename(src)
        or get_url_filename(url)
        or 'result.dat'
    )
    if mod_time and os.path.exists(fname):
        stat = os.lstat(fname)
        previous_size = stat.st_size
        previous_mod_time = datetime.datetime.utcfromtimestamp(stat.st_mtime)
        log.debug('Local  last mod %s', previous_mod_time)
        log.debug('Remote last mod %s', mod_time)
        log.debug('Local  size %d', previous_size)
        log.debug('Remote size %d', content_length)
        if not replace_newer and not touch_older:
            raise RuntimeError("%s exists" % fname)
        current = (
            replace_newer
            and previous_mod_time >= mod_time
            and previous_size == content_length
        )
        if current:
            log.info('File is current')
            return
        just_needs_touching = (
            touch_older
            and previous_mod_time > mod_time
            and previous_size == content_length
        )
        if just_needs_touching:
            log.info('Local file appears newer than remote - updating mod time')
            jaraco.path.set_time(fname, mod_time)
            return
    log.info('Downloading %s (last mod %s)', url, str(mod_time))
    dest = open(fname, 'wb')
    for line in src:
        dest.write(line)
    dest.close()
    if mod_time:
        jaraco.path.set_time(fname, mod_time)
    return fname


def print_headers(url):
    parsed = urllib.parse.urlparse(url)
    conn_class = dict(
        http=http_client.HTTPConnection, https=http_client.HTTPSConnection
    )
    conn = conn_class[parsed.scheme](parsed.netloc)
    selector = parsed.path or '/'
    if parsed.query:
        selector += '?' + parsed.query
    conn.request('HEAD', selector)
    response = conn.getresponse()
    if response.status == 200:
        print(response.msg)


def _get_url_from_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    return args.url


def wget():
    get_url(_get_url_from_command_line())


def headers():
    print_headers(_get_url_from_command_line())
