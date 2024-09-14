import time
import requests
from bs4 import BeautifulSoup
from db import documents_collection

from uuid import uuid4



def scrape_news():
    while True:
        try:
            response = requests.get("https://www.theguardian.com/international")
            response.raise_for_status()
            print(f"Status Code: {response.status_code}")
            soup = BeautifulSoup(response.text, "html.parser")
            headlines = soup.find_all("h3")

            if not headlines:
                print("No headlines found")

            for headline in headlines:
                title = headline.get_text(strip=True)

                if documents_collection.find_one({"title": title}):
                    print(f"Document with title '{title}' already exists. Skipping.")
                    continue

                link = headline.find_parent("a")
                if link and "href" in link.attrs:
                    article_url = link["href"]
                    if not article_url.startswith("http"):
                        article_url = "https://www.theguardian.com" + article_url

                    article_response = requests.get(article_url)
                    article_soup = BeautifulSoup(article_response.text, "html.parser")
                    content_div = article_soup.find(
                        "div", class_="article-body-commercial-selector"
                    )

                    if content_div:
                        paragraphs = content_div.find_all("p")
                        content_text = " ".join(
                            [p.get_text(strip=True) for p in paragraphs]
                        )
                    else:
                        content_text = ""

                    if content_text:
                        doc = {
                            "title": title,
                            "content": content_text,
                        }
                        documents_collection.insert_one(doc)

                    else:
                        print(
                            f"Skipping document with headline '{title}' due to lack of content."
                        )

        except requests.RequestException as e:
            print(f"Request error: {e}")

        time.sleep(60)
