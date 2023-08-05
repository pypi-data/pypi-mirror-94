import requests
from typing import Optional
from bs4 import BeautifulSoup
import logging


def _parse_comic_page(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")

    # Check OGP image
    url = soup.head.find(property="og:image").get("content")
    if url:
        return url

    # Check twitter embed image
    url = soup.head.find("meta", {"name": "twitter:image"}).get("content")
    if url:
        return url

    # Check comic image, outer
    url = soup.find("div", {"class": "comic"}).get("data-image")
    if url:
        return url

    # Check comic image, inner
    url = soup.find("picture", {"class": "item-comic-image"}).find("img").get("src")
    if url:
        return url

    # If we find nothing, return None
    return None


def fetch_url(comic: str, datestr: str) -> Optional[str]:
    """
    Fetch image URL for a given date of a comic from gocomics.com

    Arguments:
    comic -- URL slug of the comic, can be copied from gocomics URLs.
    datestr -- Date of the requested comic. Format is YYYY/MM/DD or YYYY-MM-DD.
    """
    url = "https://www.gocomics.com/{}/{}".format(comic, datestr.replace("-", "/"))
    req = requests.get(
        url,
        allow_redirects=False,
    )

    if req.status_code != 200:
        # TODO: This isn't ideal.
        logging.error(
            "Got {} when trying to fetch {}: {}".format(req.status_code, url, req.text)
        )
        return None

    return _parse_comic_page(req.text)
