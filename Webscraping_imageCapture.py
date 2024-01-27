import os
import requests
from bs4 import BeautifulSoup
from proxycrawl.proxycrawl_api import ProxyCrawlAPI

OUTPUT_CLASS = "invalid"

output_directory1 = os.path.join("D:/Deep learning/Invalid dataset/invalid", OUTPUT_CLASS)
os.makedirs(output_directory1, exist_ok=True)


MASTER_DICT = {"cartoon" : 50,
               "cars": 50,
               "fruits" : 50,
               "electronics": 50,
               "money" : 50,
               "travel": 50,
               "people" : 50,
               "pens": 50,
               "schools" : 50,
               "pills": 50,
               "trees" : 50,
               "bikes": 50,
               "beds" : 50,
               "random": 50,
               "numbers" : 50,
               "choclates": 50,
               "flags" : 50,
               "houses": 50,
               "animals" : 50,
               "food": 50
               }
"""
  In addition, we also gather images to build the invalid image dataset.
"""
Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

global_count = 0
for search_term in MASTER_DICT.keys():
  
  print("Processing.... Search Term:", search_term)

  num_images = MASTER_DICT[search_term]

  # Creating the query for the image
  print('Searching Images....')
  search_url = Google_Image + 'q=' + search_term
  api = ProxyCrawlAPI({'token':'OrS9jiy3f3ISiX61X23pRg', "timeout": 600})
  response = api.get(search_url, {'scroll': 'true', 'scroll_interval': '60', 'ajax_wait': 'true'})
  
  if response['status_code'] == 200:
      b_soup = BeautifulSoup(response['body'], 'html.parser') 
      results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
      
      count = 0
      imagelinks= [] # Create array to hold image links
      for res in results:
          try:
              link = res['data-src']
              imagelinks.append(link)
              count = count + 1
              if(count % 50 == 0):
                print(str(count) + " / " + str(num_images) + " found.")
              if (count >= num_images):
                  break
              
          except KeyError:
              continue
      print(f'Found {len(imagelinks)} images')
      print('Start downloading...')
      
      # Use a request to download the image
      for i, imagelink in enumerate(imagelinks):
          response = requests.get(imagelink)

          # Open each image link and save the file
          imagename = os.path.join(output_directory1, f'{OUTPUT_CLASS}_{global_count + 1}.jpg')
          global_count += 1
          with open(imagename, 'wb') as file:
              file.write(response.content)

          if((i+1) % 50 == 0):
            print(str(i+1) + " / " + str(num_images) + " downloaded.")

      print('Download Completed!')
      
MASTER_DICT = {"random": 50,
               "numbers" : 50,
               "choclates": 50,
               "flags" : 50,
               "houses": 50,
               "animals" : 50,
               "food": 50,
               }

"""
  Gathering additional invalid images.
"""

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

global_count = 529
for search_term in MASTER_DICT.keys():
  
  print("Processing.... Search Term:", search_term)

  num_images = MASTER_DICT[search_term]

  # Creating the query for the image
  print('Searching Images....')
  search_url = Google_Image + 'q=' + search_term
  api = ProxyCrawlAPI({'token':'OrS9jiy3f3ISiX61X23pRg', "timeout": 600})
  response = api.get(search_url, {'scroll': 'true', 'scroll_interval': '60', 'ajax_wait': 'true'})
  
  if response['status_code'] == 200:
      b_soup = BeautifulSoup(response['body'], 'html.parser') 
      results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
      
      count = 0
      imagelinks= [] # Create array to hold image links
      for res in results:
          try:
              link = res['data-src']
              imagelinks.append(link)
              count = count + 1
              if(count % 50 == 0):
                print(str(count) + " / " + str(num_images) + " found.")
              if (count >= num_images):
                  break
              
          except KeyError:
              continue
      print(f'Found {len(imagelinks)} images')
      print('Start downloading...')
      
      # Use a request to download the image
      for i, imagelink in enumerate(imagelinks):
          response = requests.get(imagelink)

          # Open each image link and save the file
          imagename = os.path.join(output_directory1, f'{OUTPUT_CLASS}_{global_count + 1}.jpg')
          global_count += 1
          with open(imagename, 'wb') as file:
              file.write(response.content)

          if((i+1) % 50 == 0):
            print(str(i+1) + " / " + str(num_images) + " downloaded.")

      print('Download Completed!')
