import os
import urllib.request
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

import pandas as pd

# Specify the path to your CSV file
csv_file_path = "D:/Deep learning/GalaxyZoo1_DR_table2.csv/GalaxyZoo1_DR_table2.csv"

# Read the CSV file into a Pandas DataFrame
df_orig = pd.read_csv(csv_file_path)
def drop_items(df_orig):
    # Drop the values for which the debiased threshold is less than 0.8
    df_orig = df_orig[(df_orig['P_EL_DEBIASED'] >= 0.8) | (df_orig['P_CS_DEBIASED'] >= 0.8)]
    # Drop instances where 'UNCERTAIN' == 1 (only want elliptical and spiral from this dataset)
    df_orig = df_orig[(df_orig['UNCERTAIN'] == 0)]
    
    # Now drop unecessary columns for gathering data
    df_orig = df_orig.drop(columns = ['NVOTE', 'P_EL', 'P_CW', 'P_ACW', 'P_EDGE', 'P_DK', 'P_MG', 
                            'P_CS', 'P_EL_DEBIASED', 'P_CS_DEBIASED', 'UNCERTAIN'])
    
    # Results in dataframe of [NUMBER_GALAXIES rows x 5(ID, ra, dec, spiral, elliptical) columns]
    return df_orig.reset_index(drop = True)
    
def convert_to_dec(ra, dec):
    dec_coord = SkyCoord(ra = ra, dec = dec, unit = (u.hourangle, u.deg))
    coordinates = dec_coord.to_string('decimal').split(' ')
    ra = coordinates[0]
    dec = coordinates[1]
    return ra, dec


# After reading the CSV file into df_orig
print("Original DataFrame shape:", df_orig.shape)
print("Sample data in the original DataFrame:")
print(df_orig.head())  # Display the first few rows of the original DataFrame

# Before applying filters
print("Filtering data based on debiased values and uncertainty...")


def convert_df(df_orig):
    ra_list = df_orig['RA'].tolist()
    dec_list = df_orig['DEC'].tolist()

    converted_ra = []
    converted_dec = []

    for ra, dec in zip(ra_list, dec_list):
        new_ra, new_dec = convert_to_dec(ra, dec) # SkyCoord object
        converted_ra.append(new_ra) # Appends a string
        converted_dec.append(new_dec) # Appends a string
    
    converted_ra_df_orig = pd.DataFrame({'RA_DECIMAL':converted_ra})
    converted_dec_df_orig = pd.DataFrame({'DEC_DECIMAL':converted_dec})
    frames = [df_orig['OBJID'], converted_ra_df_orig, converted_dec_df_orig, df_orig["SPIRAL"], df_orig["ELLIPTICAL"]]
    df_orig = pd.concat(frames, axis = 1)
    return df_orig
    
# After filtering
df_filtered = drop_items(df_orig)
print("Filtered DataFrame shape:", df_filtered.shape)
print("Sample data in the filtered DataFrame:")
print(df_filtered.head())  # Display the first few rows of the filtered DataFrame

# Before converting coordinates
print("Converting coordinates from degrees to decimal units...")

df_converted = convert_df(df_filtered)
print("Converted DataFrame shape:", df_converted.shape)
print("Sample data in the converted DataFrame:")
print(df_converted.head())  # Display the first few rows of the converted DataFrame

# Before downloading images
print("Downloading images based on coordinates...")


def get_images(df_converted, NUMBER_ELLIPTICAL = 1000, NUMBER_SPIRAL = 1000):
    number_elliptical = 0
    number_spiral = 0

    spiral_done = False
    elliptical_done = False

    objid_list = df_converted['OBJID'].tolist()
    ra_list = df_converted['RA_DECIMAL'].tolist()
    dec_list = df_converted['DEC_DECIMAL'].tolist()

    elliptical_list  = df_converted["ELLIPTICAL"].tolist()
    spiral_list  = df_converted["SPIRAL"].tolist()
    
    for objid, ra, dec, spiral in zip(objid_list, ra_list, dec_list, spiral_list):
        # Save the image using the 'OBJID' as .jpg image
        if spiral_done and elliptical_done:
          break
        
        filename = str(objid) + '.jpg'
        
        if spiral:
          if spiral_done or number_spiral > NUMBER_SPIRAL:
            spiral_done = True
            continue

          filename = os.path.join("D:/Deep learning/galaxy-image-classification-main/", "spiral", filename)
          number_spiral+=1

        else:
          if elliptical_done or number_elliptical > NUMBER_ELLIPTICAL:
            elliptical_done = True
            continue

          filename = os.path.join("D:/Deep learning/galaxy-image-classification-main/", "elliptical", filename)
          number_elliptical +=1

        # Replace the ra and dec coordinates in the URL, downloading in 512 x 512 resolution
        try:
            image_url = "http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra=" + str(ra) + "&dec=" + str(dec) + "&scale=0.15&width=512&height=512&opt="
            urllib.request.urlretrieve(image_url, filename) 
            print("ObjID:", objid, "saved at:", filename)
        except:
            print("Image with object ID " + str(objid) + " and coordinates " + str(ra) + ", " + str(dec) + " not found.")
            continue # Continue to next set of coordinates and image retrieval
    
# After downloading images
get_images(df_converted)
print("Image downloading complete.")

