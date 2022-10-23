from bs4 import BeautifulSoup
import requests
import csv
import time 
import pdb
from itertools import islice
import re

## Open website and return html file
def get_site(req):
    print(req)
    try:
        page = requests.get(req, timeout=10)
        if(page.status_code != 200):
            return ''
        else:
            return BeautifulSoup(page.content, 'html.parser')
    except requests.exceptions.RequestException as error:
        print("Error: ", error)
        return ''

#Extract sub-category links 

etsy_categories = ["https://www.etsy.com/ca/c/jewelry-and-accessories?ref=catnav-10855",
                   "https://www.etsy.com/ca/c/clothing-and-shoes?ref=catnav-10923",
                  "https://www.etsy.com/ca/c/home-and-living?ref=catnav-891",
                  "https://www.etsy.com/ca/c/wedding-and-party?ref=catnav-10983",
                  "https://www.etsy.com/ca/c/toys-and-entertainment?ref=catnav-11049",
                  "https://www.etsy.com/ca/c/art-and-collectibles?ref=catnav-66",
                  "https://www.etsy.com/ca/c/craft-supplies-and-tools?ref=catnav-562"]

def extract_subcategories(category_link):
    response = requests.get(category_link)
    html = response.text
    
    soup = BeautifulSoup(html,"html.parser")
    links = soup.findAll("a")
    
    urls = []
    for link in links: 
        href = str(link.get("href"))
        if href.startswith("/ca/c/home-and-living/") and href[-1].isdigit():
            url = "https://www.etsy.com" + href 
            urls.append(url)

    return urls 
    


## Get links of listings under subcategory
def getListings(subCategoryLink):
    
    response = requests.get(subCategoryLink)
    html = response.text

    #print(html)
    
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll("a", class_="listing-link")
    
    urls = []
    for link in links: 
        href = link.get("href")
        if href.startswith("https://www.etsy.com/ca/listing/"):
            urls.append(href)
            
    return urls

#Extract checkout link information and return a json format
def extract_info(checkoutLink):
  """
   Extract the following:
         - Num of sales from <span class="wt-text-caption ">812 sales</span>
         X Product highlights
         X Delivery times
         X Cost of delivey
         - Maybe basket number
         X Number of items reviews
         X Number of show reviews
         X Rating
         X Name of item
         X Name of shop 
         X Price
  """
  response = requests.get(checkoutLink)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')


  product_name = soup.findAll("h1", class_="wt-text-body-03 wt-line-height-tight wt-break-word")
  shop_name = soup.findAll("p", class_="wt-text-body-01 wt-mr-xs-1")
  #num_sales = return_num_sales(soup)
  product_highlights = return_product_highlights(soup)
  price = return_price(soup)
  shop_reviews = soup.findAll("h2", class_="wt-mr-xs-2 wt-text-body-03")
  item_reviews = soup.findAll("span", class_="wt-badge wt-badge--status-02 wt-ml-xs-2")
  rating = soup.find("input", {"name":"rating"})["value"]
  shipping_time = soup.findAll("span", class_="wt-text-body-03 wt-mt-xs-1 wt-line-height-tight")
  delivery_fee = soup.findAll("p", class_="wt-text-body-03 wt-mt-xs-1 wt-line-height-tight")


  print(product_name[0].text)
  print(shop_name[0].text)
  #num_sales
  print(product_highlights)
  print(price)
  print(shop_reviews[0].text)
  print(item_reviews[0].text)
  print(rating)
  print(shipping_time[1].text)
  print(delivery_fee[1].text)


def return_num_sales(soup):
  """
  TODO: 
  - Differentiate between star seller, regular seller, and ads
  - Return only string
  NOTE: 
  - For best sellers class name is wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap
  - For regular sellers wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-3

  Will only be doing regular sellers for now.
  """
  #Num sales must return span tag with class name wt-text-caption
  #num_sales_row = soup.findAll("div", string="sales")
  arr = soup.findAll("div", class_="wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-2")
  for element in arr:
    """
    Return only sales
    """
    print(element)


def return_product_highlights(soup):
  """
  TODO: Only return text
  """
  return soup.findAll("div", id="product-details-content-toggle")


def return_price(soup):
  """
  Return price by looping through element
  """
  price = soup.findAll("p", class_="wt-text-title-03 wt-mr-xs-1")
  return price

  


def main():
    try:
      """
      #Go to etsy site
      #Pick a link and category
      #Grab checkout link
        Extract the following:
         Extract the following:
         - Num of sales from <span class="wt-text-caption ">812 sales</span>
         - Product highlights
         - Cost of delivey
         - Maybe basket number
         - Numbe of items reviews
         - Number of show reviews
         - Name of item
         - Name of shop
      """
      etsyCategory = "https://www.etsy.com/ca/c/jewelry-and-accessories?ref=catnav-10855"

      

      
      
      
      getListings("https://www.etsy.com/ca/c/jewelry/earrings?ref=catcard-10896-474793820&explicit=1")
      
      #extract_info("https://www.etsy.com/ca/listing/474793820/amethyst-pale-earrings-purple-stud?click_key=d59d2b3ff560cb8811ed2ea5e437d9186e5f355c%3A474793820&click_sum=979c6952&ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=listing_in_grid-1-1&frs=1")
   




    except ValueError as ve:
        return str(ve)


if __name__ == "__main__":
  main()


