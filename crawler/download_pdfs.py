import requests
import requests_cache
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import os
from datetime import date
from xml.etree.ElementTree import fromstring, ElementTree

EARLIEST_YEAR = 1801  # legislation earliest published
CURRENT_YEAR = date.today().year

year_range = range(EARLIEST_YEAR, CURRENT_YEAR)
pdfs_to_store = []

requests_cache.install_cache("legislation_cache", expire_after=(60 * 60 * 22))


def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def extract_pdf_urls_from_xml(file_contents):
    tree = ElementTree(fromstring(file_contents))
    root = tree.getroot()

    pdf_urls_found = []
    for item in root.iter("{http://www.w3.org/2005/Atom}link"):
        link_type = item.attrib.get("type")
        if link_type == "application/pdf":
            pdf_url = item.attrib.get("href")
            pdf_urls_found.append(pdf_url)
    return pdf_urls_found


def get_pdfs_for_year(year):
    primary_url_to_crawl = f"https://www.legislation.gov.uk/ukpga/{year}/data.feed"
    try:
        response = requests_retry_session().get(primary_url_to_crawl)
    except Exception as x:
        print("It failed :(", x.__class__.__name__)
    file_text = response.content
    print(primary_url_to_crawl)
    pdf_urls_found = extract_pdf_urls_from_xml(file_text)
    return pdf_urls_found


for year in year_range:
    pdfs_to_store.extend(get_pdfs_for_year(year))

if not os.path.exists("download"):
    os.makedirs("download")

total_pdfs = len(pdfs_to_store)
completed_pdfs = 0
for pdf_url in pdfs_to_store:
    filename = pdf_url.replace("http://www.legislation.gov.uk/", "").replace("/", ".")
    with requests_retry_session().get(pdf_url, stream=True) as r:
        with open(f"download/{filename}", "wb") as f:
            for chunk in r.iter_content(chunk_size=16 * 1024):
                f.write(chunk)
    completed_pdfs += 1
    if (completed_pdfs % 10) == 0:
        print(f"Total pdfs {total_pdfs}, and {completed_pdfs} downloaded so far.")

print("All PDFs downloaded.")