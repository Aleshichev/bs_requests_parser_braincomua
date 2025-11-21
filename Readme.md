# Brain.com.ua Parser

Web scraper for collecting product information from brain.com.ua using BeautifulSoup4 / requests and Django ORM.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
poetry install

```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
POSTGRES_DB=your-db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
```

### 3. Start Database

```bash
docker-compose up -d
```

### 4. Django Migrations

```bash
cd braincomua_bs_project
python manage.py migrate
```

### 5. Run Parser

```bash
# From project root
python modules/1_bs_parser.py
```

## 🔧 Features

- ✅ Search products by name
- ✅ Collect full product information (title, price, photos, specifications)
- ✅ Save to PostgreSQL
- ✅ Export to CSV
- ✅ Playwright anti-detection settings
- ✅ Logging of all operations

## 📊 Collected Data

- Product title
- Price (regular/sale)
- Photos (all)
- Product code
- Review count
- Specifications (processor, memory, screen, etc.)
- Manufacturer, color, memory, screen diagonal

## ⚙️ Configuration


### \xa0 Character in Data

Add cleanup in `parse_specification_row`:

```python
text = text.replace('\xa0', ' ').strip()
```

## 📝 Dependencies

- Python 3.10+
- Django 5.2.8
- Beautifulsoup4 4.14.2
- PostgreSQL 15
- pandas 2.3.3
- requests = 2.32.5
- lxml = 6.0.2

## 👨‍💻 Author

Igor Aleshichev

## 📄 License

MIT