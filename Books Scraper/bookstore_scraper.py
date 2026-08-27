from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import csv

def book_scraper(url):
  # Network layer
  try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    raise RuntimeError(f"Failed to fetch {url}") from e

  # Parsing layer
  soup = BeautifulSoup(response.text, "html.parser")
  books = soup.find_all("article", class_="product_pod")

  result = []
  for book in books:
    try:
      header = book.find("h3")
      link_tag = header.find("a") if header else None
      # Title
      title = link_tag.get("title", "n/a").strip() if link_tag else "n/a"

      # Price
      price_tag = book.find("p", class_="price_color")
      price = price_tag.text.strip()[1:] if price_tag else "n/a"

      # Link
      href = link_tag.get("href", "") if link_tag else ""
      full_link = url + href if href else "n/a"

      # Timestamp
      timestamp = datetime.now().isoformat()
      result.append({
          "title": title,
          "price": price,
          "link": full_link,
          "timestamp": timestamp
      })

    except Exception as e:
      print(f"Skipping a book due to parsing error: {e}")

  return result


def save_to_csv(file_path, data):
  try:
    with open(file_path, "w", newline="", encoding="utf-8") as file:
      writer = csv.DictWriter(file, fieldnames=["title", "price", "link", "timestamp"])
      writer.writeheader()
      writer.writerows(data)
    print(f"Saved data to {file_path}")
  except IOError as e:
    print(f"Error writing CSV file: {e}")


def save_to_json(file_path, data):
  try:
    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(data, file, indent=2)
    print(f"Saved data to {file_path}")
  except IOError as e:
    print(f"Error writing JSON file: {e}")


if __name__ == "__main__":
    url = "https://books.toscrape.com" 

    books = []
    try:
        books = book_scraper(url)
    except Exception as e:
        print(f"Error during scraping: {e}")

    # User choice
    choose_format = input("Choose a format (CSV or JSON): ").strip().lower()

    if choose_format == "csv":
        save_to_csv("books.csv", books)
    elif choose_format == "json":
        save_to_json("books.json", books)
    else:
        print("Invalid format. Please choose 'CSV' or 'JSON'.")

