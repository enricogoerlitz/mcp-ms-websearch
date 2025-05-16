import io
import re
import requests
import pdfplumber
import gvars

from collections import Counter
from bs4 import BeautifulSoup
from pdfplumber.page import Page
from urllib.parse import urlparse

from typing import Iterator


def read_web_pdf_pages(resp: requests.Response) -> Iterator[Page] | None:
    if resp.status_code > 400:
        return None

    pdf_file = io.BytesIO(resp.content)
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            yield page


def get_web_pdf_size(url: str) -> int | None:
    response = requests.head(url)
    if response.status_code >= 400:
        return None

    if "Content-Length" in response.headers:
        return int(response.headers["Content-Length"])  # Size in bytes

    return None


def get_host_url(url: str) -> str:
    parsed_url = urlparse(url)
    host = f"{parsed_url.scheme}://{parsed_url.netloc}"

    return host


def compress_soup_text(soup: BeautifulSoup) -> str:
    for tag in soup(["a", "script", "style", "meta", "noscript", "footer", "header", "nav"]):
        tag.decompose()

    # Extract text and normalize whitespace
    text = soup.get_text("\n\n", strip=True)
    text = re.sub(r" {2,}", "", text)
    text = re.sub(r"\t{2,}", "\t", text)
    text = re.sub(r"\n{2,}", "\n\n", text)

    # Remove stopwords to reduce unnecessary words
    text = " ".join([word for word in text.split() if word.lower() not in gvars.STOP_WORDS])

    # Deduplicate sentences based on frequency
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentence_counts = Counter(sentences)
    text = " ".join(sentence_counts.keys())

    return text.strip()
