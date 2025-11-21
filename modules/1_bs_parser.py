import logging

import requests
from bs4 import BeautifulSoup
from config.headers import headers, url
from config.logger_config import setup_logging
from load_django import *
from utils.get_informations import collect_product_data
from utils.storage import export_to_csv, save_to_database

logger = setup_logging()


def main():
    logging.info("Starting request to URL")

    try:
        resp = requests.get(url, headers=headers, timeout=40)
        resp.raise_for_status()
        logging.info("Request to URL successful")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")

    html = resp.text

    # # with open("files/page.html", "w", encoding="utf-8") as f:
    # #     f.write(html)

    # with open("files/page.html", "r", encoding="utf-8") as f:
    #     html = f.read()

    soup = BeautifulSoup(html, "lxml")

    product_data = collect_product_data(soup)

    save_to_database(product_data)
    export_to_csv()

    logging.info("Finished")


if __name__ == "__main__":
    main()
