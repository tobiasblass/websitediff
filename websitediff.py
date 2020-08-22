#!/usr/bin/env python3

import requests
from pathlib import Path
from os import environ
import difflib
from urllib.parse import urlparse
import time
import sys

cache_dir = Path(environ.get('XDG_CACHE_HOME', Path.home()/".cache"), "websitediff")
config_file = Path(environ.get('XDG_CONFIG_HOME', Path.home()/".config"), "websitediff.conf")

#Change this variable to print the website diff in textual form. Disabled by default
print_diff = False

def website_cache_file(url):
    _,loc,path,*ignore = urlparse(url)
    if path and path[0] == '/':
        path = path[1:]
    cache_file = (cache_dir/loc/path).resolve()
    #Sanity check: cache_file is below cache_dir.
    try:
        cache_file.relative_to(cache_dir)
    except ValueError:
        raise RuntimeError(f'Cache file for {url} is {cache_file}, which is not below {cache_dir}. This should be impossible! Aborting to prevent data loss.')

    return cache_file
    
def diff_website(url, store_new=True):
    diff = None
    req = requests.get(url)
    req.raise_for_status()

    cache_file = website_cache_file(url)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    if cache_file.exists():
        diff = difflib.unified_diff(cache_file.read_text().split('\n'),
                                    req.text.split('\n'),
                                    fromfile=url,
                                    tofile=url,
                                    lineterm='',
                                    fromfiledate=time.ctime(cache_file.stat().st_mtime),
                                    tofiledate=time.ctime())


    if store_new:
        try:
            cache_file.unlink()
        except FileNotFoundError:
            pass
        with cache_file.open(mode='x') as fp:
            fp.write(req.text)
    
    return diff

def main(urls=None):
    if urls is None:
        with config_file.open() as config:
            urls = list(config)
    for url in urls:
        if 'http' not in url:
            url = f'https://{url}'
        lines = diff_website(url)
        if lines:
            if print_diff:
                print('\n'.join(lines))
            else:
                print(url)

if __name__ == '__main__':
    cmdline_urls = ([arg for arg in sys.argv[1:] if arg and arg[0] != '-'] or
                    None)

    main(urls=cmdline_urls)
