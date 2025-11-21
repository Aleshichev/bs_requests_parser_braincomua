"""
Module for collecting product data using Selenium.
"""

import logging
import re


def clean_text(text):
    """Clean and normalize text."""
    if not text:
        return text
    text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def get_product_title(soup: str):
    """Extract product title"""

    try:
        title = soup.select_one("div.main-right-block h1.desktop-only-title")
        if not title:
            logging.error("Product title not found.")
            return None

        title_text = title.get_text(strip=True)
        logging.info(f"Product title found: {title_text}")
        return title_text

    except Exception as e:
        logging.error(f"Error while parsing title: {e}")
        return None


def get_product_price(soup: str):
    """Extract product regular price."""

    try:
        price_block = soup.select_one(
            "div.br-pr-price.main-price-block div.price-wrapper"
        )
        if not price_block:
            logging.error("Price not found.")
            return None

        price_text = price_block.get_text(strip=True).replace("\n", "")
        price_text = re.sub(r"[^\d.,]", "", price_text)
        price_text = price_text.replace(",", ".")
        price_float = float(price_text)
        logging.info(f"Price found: {price_float}")
        return price_float

    except Exception as e:
        logging.error(f"Error while parsing price: {e}")
        return None


def get_product_photos(soup: str):
    """Extract all product photos."""
    try:
        photo_elements = soup.select(
            "div.product-block-right a.product-modal-button img"
        )

        photos = []
        for img in photo_elements:
            src = img.get("src")
            if src:
                photos.append(src)

        logging.info(f"Added {len(photos)} photos.")
        return photos

    except Exception as e:
        logging.error(f"Error while parsing photos: {e}")
        return []


def get_review_count(soup: str):
    """Extract review count."""
    try:
        review_count = soup.select_one(
            "div.fast-navigation-comments-body a.scroll-to-element.reviews-count span"
        )
        count = int(review_count.text.strip())
        logging.info(f"Review count found: {count}")
        return count
    except Exception as e:
        logging.error("Review count not found {e}.")
        return None


def get_product_code(soup):
    """Extract product code using BeautifulSoup."""
    try:
        code_span = soup.select_one("div.title span.br-pr-code-val")
        if code_span is None:
            logging.warning("Product code not found.")
            return None

        code_text = code_span.get_text(strip=True)
        logging.info(f"Product code found: {code_text}")
        return code_text

    except Exception as e:
        logging.error(f"Error while parsing product code: {e}")
        return None


def parse_specification_row(row):
    spans = row.find_all("span")
    if len(spans) < 2:
        return None, None

    key = spans[0].get_text(strip=True)

    values = []

    for span in spans[1:]:
        links = span.find_all("a")
        if links:
            for a in links:
                values.append(a.get_text(strip=True))
        else:
            text_val = span.get_text(strip=True)
            if text_val:
                values.append(text_val)

    value = ", ".join(values)

    return key, value


def parse_specification_detail(item):
    section_title = item.find("h3").get_text(strip=True)
    section_dict = {}

    rows = item.select("div > div")

    for row in rows:
        key, value = parse_specification_row(row)
        if key:
            section_dict[key] = clean_text(value)

    return {section_title: section_dict}


def get_product_specifications(soup):
    """Extract all product specifications using BeautifulSoup."""
    try:
        specification_blocks = soup.select(
            "div.br-pr-scroll.br-loading.br-pr-no-scroll"
        )
        if not specification_blocks:
            logging.warning("No specification blocks found.")
            return {}

        specs_dict = {}

        for block in specification_blocks:
            try:
                details = block.select("div.br-pr-chr-item")

                for detail in details:
                    detail_specs = parse_specification_detail(detail)
                    specs_dict.update(detail_specs)

                logging.info("Collected details for one specification block.")

            except Exception as e:
                logging.error(f"Error parsing specification block: {e}")
                continue

        logging.info(f"Collected {len(specs_dict)} specification sections.")
        return specs_dict

    except Exception as e:
        logging.error(f"Error while parsing specifications: {e}")
        return {}


def extract_specific_specs(specifications):
    """Extract specific specifications from the full specs dictionary."""
    specific_data = {}

    try:
        specific_data["manufacturer"] = specifications.get("Інші", {}).get("Виробник")
    except Exception as e:
        logging.warning(f"Could not extract manufacturer: {e}")
        specific_data["manufacturer"] = None

    try:
        specific_data["memory"] = specifications.get("Функції пам'яті", {}).get(
            "Вбудована пам'ять"
        )
    except Exception as e:
        logging.warning(f"Could not extract memory: {e}")
        specific_data["memory"] = None

    try:
        specific_data["color"] = specifications.get("Фізичні характеристики", {}).get(
            "Колір"
        )
    except Exception as e:
        logging.warning(f"Could not extract color: {e}")
        specific_data["color"] = None

    try:
        specific_data["screen_diagonal"] = specifications.get("Дисплей", {}).get(
            "Діагональ екрану"
        )
    except Exception as e:
        logging.warning(f"Could not extract screen diagonal: {e}")
        specific_data["screen_diagonal"] = None

    try:
        specific_data["screen_resolution"] = specifications.get("Дисплей", {}).get(
            "Роздільна здатність екрану"
        )
    except Exception as e:
        logging.warning(f"Could not extract screen resolution: {e}")
        specific_data["screen_resolution"] = None

    return specific_data


def collect_product_data(soup):
    """Collect product data from the product page."""
    logging.info("Start collecting product data...")

    product_data = {}

    # Basic product information
    product_data["title"] = get_product_title(soup)
    product_data["regular_price"] = get_product_price(soup)
    product_data["sale_price"] = None
    product_data["photos"] = get_product_photos(soup)
    product_data["review_count"] = get_review_count(soup)
    product_data["code"] = get_product_code(soup)

    # # Collect specifications
    product_data["specifications"] = get_product_specifications(soup)

    # Extract specific specifications
    specific_specs = extract_specific_specs(product_data["specifications"])
    product_data.update(specific_specs)

    print(product_data)
    return product_data
