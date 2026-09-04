from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import csv


def scrape_page(driver):
  html=driver.page_source
  soup=BeautifulSoup(html,"html.parser")
  books=soup.find_all("article", class_="product_pod")

  products=[]
  for book in books:
    title=book.find("img")["alt"]
    print(title)
    price=book.find("p", class_="price_color")
    print(price)
    price=price.text
    available=book.find("p", class_="instock availability").text.strip()
    products+=[{"title":title,"price":price,"available":available}]
  return products

def go_to_next_page(driver):
  try:
    button_next=driver.find_element(By.CLASS_NAME,"next").find_element(By.TAG_NAME,"a")
    button_next.click()
    return True
  except:
    return False

def save_to_csv(file_path, data):
  try:
    with open(file_path, "w", newline="", encoding="utf-8") as file:
      writer = csv.DictWriter(file, fieldnames=data[0][0].keys())
      writer.writeheader()
      for row in data:
        writer.writerows(row)
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
    url="https://books.toscrape.com/"
    driver=webdriver.Chrome()
    driver.get(url)

    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    books=soup.find_all("article", class_="product_pod")
    print(len(books))
    all_products=[] 
    page=1
    while True:
        print(page)
        all_products.append(scrape_page(driver))
        if not go_to_next_page(driver):
            break
        page+=1
    choice=input("Choose the format to save your data (csv or json): ")
    if choice.lower()=="csv":
      save_to_csv(Path(__file__).resolve().parent / "data.csv", all_products)
    elif choice.lower()=="json":
      save_to_json(Path(__file__).resolve().parent / "data.json", all_products)
    else:
      print("Invalid format.")
    
    print(all_products)




