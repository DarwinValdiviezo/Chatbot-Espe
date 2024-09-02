# web_scraper_test.py
from app.utils.web_scraper import search_espe_website

query = "filosofia institucional de la universidad espe"
result = search_espe_website(query)
print(f"Web search result: {result}")
