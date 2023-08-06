def PRODUCT_NAME(container):
      try:
         x = container.div.span.div.div.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text.strip()
      except AttributeError:
                 x = "Not Available" 
      return x 
def PRICE(container):
     try:
      u = container.div.span.div.div.find("span", {"class": "a-price-whole"}).text.strip()
     except AttributeError:
         u = "Not Available"
     return u  
def RATINGS(container):
     try:
      j = container.find("span", {"class": "a-icon-alt"}).text.strip()
     except AttributeError:
         j = "Not Available"
     return j
def AVAILABILITY(container):
     try:
      l = container.find("span", {"class": "a-color-price"}).text.strip()
     except:
          l = "Available"
     return l