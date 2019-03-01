import sys
import argparse
from datetime import datetime
import requests
import whois
from urllib.parse import urlparse
from texttable import Texttable


def load_urls4check(path):
    with open(path, "r", encoding="utf8") as fh:
        return [line.strip() for line in fh.readlines()]


def get_domain_from_url(url):
    parsed_uri = urlparse(url)
    return parsed_uri.netloc


def is_server_respond_with_200(url):
    try:
        return requests.get(url).ok
    except requests.exceptions.RequestException:
        return False


def get_domain_expiration_date(domain_name):
    try:
        domain = whois.whois(domain_name)
    except whois.parser.PywhoisError:
        return None
    except ConnectionResetError:
        return None

    if isinstance(domain.expiration_date, list):
        return domain.expiration_date[0]

    return domain.expiration_date


def is_domain_prepaid(expiration_date, prepaid_days_min=30):
    remain_time = (expiration_date - datetime.now())
    return remain_time.days > prepaid_days_min


def get_url_info(url):
    domain_name = get_domain_from_url(url)
    expiration_date = get_domain_expiration_date(domain_name)
    is_available = is_server_respond_with_200(url)

    if expiration_date:
        is_prepaid = is_domain_prepaid(expiration_date)
    else:
        is_prepaid = False

    return {
        "domain_name": domain_name,
        "is_available": is_available,
        "is_prepaid": is_prepaid,
        "expiration_date": expiration_date
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="Path to file with list urls")
    args = parser.parse_args()

    try:
        url_list = load_urls4check(args.src)
    except FileNotFoundError:
        sys.exit("File not found")

    result_table = Texttable()
    result_table.set_deco(Texttable.HEADER)
    result_table.add_row(
        ["Domain", "Is available", "Is prepaid", "Expiration date"]
    )

    for url in url_list:
        url_info = get_url_info(url)
        result_table.add_row(
            [
                url_info["domain_name"],
                "Yes" if url_info["is_available"] else "No",
                "Yes" if url_info["is_prepaid"] else "No",
                url_info["expiration_date"]
            ]
        )

    print(result_table.draw())


if __name__ == '__main__':
    main()
