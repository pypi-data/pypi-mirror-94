import requests
from typing import Optional, List
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


def _gocomics_request(url) -> requests.models.Response:
    req = requests.get(
        url,
        allow_redirects=False,
    )

    assert req.status_code == 200
    return req


def fetch_calendar(comic: str, datestr: str) -> List[str]:
    """
    Fetch a list of days with comics in a given month

    Arguments:
    comic -- URL slug of the comic, can be copied from gocomics URLs.
    datestr -- Year and month of the requested calendar. Format is YYYY/MM or YYYY-MM.
    """
    url = "https://www.gocomics.com/calendar/{}/{}".format(
        comic, datestr.replace("-", "/")
    )
    req = _gocomics_request(url)

    return req.json()


def fetch_url(comic: str, datestr: str) -> Optional[str]:
    """
    Fetch image URL for a given date of a comic from gocomics.com

    Arguments:
    comic -- URL slug of the comic, can be copied from gocomics URLs.
    datestr -- Date of the requested comic. Format is YYYY/MM/DD or YYYY-MM-DD.
    """
    url = "https://www.gocomics.com/{}/{}".format(comic, datestr.replace("-", "/"))
    req = _gocomics_request(url)

    return _parse_comic_page(req.text)
