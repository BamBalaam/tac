"""Scraping the AVB for PDFs of bulletins"""

import os
from pathlib import Path
import re
import time
import sys

import requests


def get_urls():
    """Retrieve all URLs from root AVB page"""
    root_url = "https://archives.bruxelles.be/bulletins/date"
    resp = requests.get(root_url)
    print(f"Status: {resp.status_code}")
    print(f"Encoding: {resp.encoding}")
    html = resp.text
    print(f"Text length: {len(html)}")

    pattern = r"https://archief.brussel.be/Colossus/BulletinsCommunaux/Bulletins/Documents/.*\.pdf"
    urls = re.findall(pattern, html)
    print(f"{len(urls)} PDF files found")
    return urls


def get_filenames_from_urls(urls):
    """ Returns a list of filenames from a list of urls"""
    return [url.split("/")[-1] for url in urls]


def get_undownloaded_files(urls, already_downloaded):
    """ Returns a list of undownloaded files"""
    diff = list(
        set(urls) - set(already_downloaded)
    )
    return diff


def download(urls, filenames, downloads):
    """Dowloading files which weren't already"""
    undownloaded = get_undownloaded_files(filenames, downloads)
    for url in urls:
        filename = url.split("/")[-1]
        if filename in undownloaded:
            print(f"Dowloading {filename}...")
            start_time = time.time()
            response = requests.get(url)
            print(f"   done in {(time.time() - start_time):.1f} seconds")
            with open(f"data/pdf/{filename}", 'wb') as f:
                f.write(response.content)


def check(filenames, downloads):
    """Check if all files have been downloaded"""
    diff = get_undownloaded_files(filenames, downloads)
    for missing_file in diff:
        print(f"{missing_file} is missing!")
    print(f"{len(diff)} PDFs missing out of {len(filenames)}!")


if __name__ == "__main__":
    try:
        task = sys.argv[1]
    except IndexError:
        print("No task provided, please use either 'download' or 'check'")
        sys.exit(1)
    all_urls = get_urls()
    Path("data/pdf").mkdir(parents=True, exist_ok=True)
    filenames = get_filenames_from_urls(all_urls)
    downloads = os.listdir('data/pdf')
    if task == "download":
        download(all_urls, filenames, downloads)
        check(filenames, downloads)
    elif task == "check":
        check(filenames, downloads)
    else:
        print("Unknown task, please use either 'download' or 'check'")
        sys.exit(1)
