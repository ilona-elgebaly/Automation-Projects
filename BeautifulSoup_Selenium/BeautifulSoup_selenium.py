from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import csv

options=Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disabled-dev-shm-usage")

url="https://books.toscrape.com/"
driver=webdriver.Chrome(options=options)
driver.get(url)

html=driver.page_source
soup=BeautifulSoup(html,"html.parser")
books=soup.find_all("article", class_="product_pod")
print(len(books))

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

  
page=1
while True:
  print(page)
  all_products.append(scrape_page(driver))
  if not go_to_next_page(driver):
    break
  page+=1
print(all_products)

