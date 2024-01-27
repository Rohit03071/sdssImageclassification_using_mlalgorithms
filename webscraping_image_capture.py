import os
import requests
from bs4 import BeautifulSoup
from proxycrawl.proxycrawl_api import ProxyCrawlAPI

OUTPUT_CLASS = "irregular"

# Create a dictionary with the image type and the number of images you would like to download
MASTER_DICT = {"Irregular galaxies" : 50,
               "Hubble Irregular galaxies ": 25,
               "Faulkes Irregular galaxies ": 25,
               "NASA Irregular galaxies": 25,
               "ESA Irregular galaxies": 25,
               "ISRO Irregular galaxies": 25,
               "JAXA Irregular galaxies": 25,
               "CNSA Irregular galaxies": 25,
               "ROSCOSMOS Irregular galaxies": 25
               }

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

output_directory = os.path.join("D:/Deep learning/Irregular Galaxies/irregular", OUTPUT_CLASS)
os.makedirs(output_directory, exist_ok=True)

global_count = 0
for search_term in MASTER_DICT.keys():
  
  print("Processing.... Search Term:", search_term)

  num_images = MASTER_DICT[search_term]

  # Creating the query for the image
  print('Searching Images....')
  search_url = Google_Image + 'q=' + search_term
  api = ProxyCrawlAPI({'token':'OrS9jiy3f3ISiX61X23pRg', "timeout": 600})
  response = api.get(search_url, {'scroll': 'true', 'scroll_interval': '60', 'ajax_wait': 'true'})
  #we are looking for resonses with status code 200, which is implication of success value
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
      
      for i, imagelink in enumerate(imagelinks):
          response = requests.get(imagelink)

          # Open each image link and save the file
          imagename = os.path.join(output_directory, f'{OUTPUT_CLASS}_{global_count + 1}.jpg')
          global_count += 1
          with open(imagename, 'wb') as file:
              file.write(response.content)

          if((i+1) % 50 == 0):
            print(str(i+1) + " / " + str(num_images) + " downloaded.")

      print('Download Completed!')
