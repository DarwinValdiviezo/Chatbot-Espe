# app/utils/web_search.py

import requests
from bs4 import BeautifulSoup

def search_espe_website(query):
    query = query.lower()
    url = "https://www.espe.edu.ec/search?q=" + query.replace(" ", "+")
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        relevant_texts = []
     
        for paragraph in paragraphs:
            text = paragraph.get_text().strip().lower()
            if query in text:
                relevant_texts.append(text)
     
        if not relevant_texts:
            titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for title in titles:
                text = title.get_text().strip().lower()
                if query in text:
                    relevant_texts.append(text)
     
        if relevant_texts:
            return ' '.join(relevant_texts).capitalize() + "..."
        else:
            return None
 
    return None
