from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os

# Set up ChromeDriver
chrome_driver_path = 'C:\\chromedriver\\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the ESRB search page
url = "https://www.esrb.org/search/?searchKeyword=&platform=All%20Platforms&rating=E%2CE10%2B%2CT%2CM&descriptor=All%20Content&pg=1&searchType=LatestRatings&ielement[]=UIN&ielement[]=IGP&ielement[]=IGPR&timeFrame=All"
driver.get(url)

# Wait for the page to load the games
time.sleep(5)

# Prepare lists for scraped data
data = []

# Define the columns matching your CSV structure
columns = ['title', 'console', 'alcohol_reference', 'animated_blood', 'blood', 'blood_and_gore',
           'cartoon_violence', 'crude_humor', 'drug_reference', 'fantasy_violence', 'intense_violence',
           'language', 'mild_blood', 'mild_cartoon_violence', 'mild_fantasy_violence', 'mild_language',
           'mild_lyrics', 'mild_suggestive_themes', 'mild_violence', 'nudity', 'sexual_content',
           'sexual_themes', 'simulated_gambling', 'strong_language', 'strong_sexual_content',
           'suggestive_themes', 'use_of_alcohol', 'use_of_drugs_and_alcohol', 'violence', 'esrb_rating']

# Mapping for content descriptors to match your CSV column names
descriptor_mapping = {
    'Alcohol Reference': 'alcohol_reference',
    'Animated Blood': 'animated_blood',
    'Blood': 'blood',
    'Blood and Gore': 'blood_and_gore',
    'Cartoon Violence': 'cartoon_violence',
    'Crude Humor': 'crude_humor',
    'Drug Reference': 'drug_reference',
    'Fantasy Violence': 'fantasy_violence',
    'Intense Violence': 'intense_violence',
    'Language': 'language',
    'Mild Blood': 'mild_blood',
    'Mild Cartoon Violence': 'mild_cartoon_violence',
    'Mild Fantasy Violence': 'mild_fantasy_violence',
    'Mild Language': 'mild_language',
    'Mild Lyrics': 'mild_lyrics',
    'Mild Suggestive Themes': 'mild_suggestive_themes',
    'Mild Violence': 'mild_violence',
    'Nudity': 'nudity',
    'Sexual Content': 'sexual_content',
    'Sexual Themes': 'sexual_themes',
    'Simulated Gambling': 'simulated_gambling',
    'Strong Language': 'strong_language',
    'Strong Sexual Content': 'strong_sexual_content',
    'Suggestive Themes': 'suggestive_themes',
    'Use of Alcohol': 'use_of_alcohol',
    'Use of Drugs and Alcohol': 'use_of_drugs_and_alcohol',
    'Violence': 'violence',
    'ESRB Rating': 'esrb_rating'
}

# CSV file name
csv_filename = 'data/esrb_ratings_scraped.csv'

# Function to scrape data from a single page
def scrape_page():
    # Find all games listed on the page
    games = driver.find_elements(By.CLASS_NAME, 'game')
    print(f"Number of games found: {len(games)}")

    # Loop through each game and extract relevant data
    for game in games:
        # Extract the game title and platform information
        title = game.find_element(By.CSS_SELECTOR, 'h2').text.strip()
        console = game.find_element(By.CLASS_NAME, 'platforms').text.strip()
        # print(f"Title: {title}, Platform: {console}")
        
        # Find the content section with descriptors
        content_section = game.find_element(By.CLASS_NAME, 'content')
        rows = content_section.find_elements(By.TAG_NAME, 'tr')
        
        # Extract the rating from the 'alt' attribute of the img tag
        rating_img = rows[1].find_element(By.TAG_NAME, 'img')
        rating = rating_img.get_attribute('alt')
        
        # Check if rating is "E10+" and change it to "ET"
        if rating == "E10+":
            rating = "ET"
        
        # Extract the content descriptors
        descriptors = rows[1].find_elements(By.TAG_NAME, 'td')[1].text.strip()

        # Clean the descriptors to remove newline characters
        descriptors = descriptors.replace('\n', '').strip()
        descriptor_list = [d.strip() for d in descriptors.split(",")]

        # print(f"Original Descriptors: {descriptor_list}")

        # Create a dictionary for each game with 0 for all descriptors initially
        game_data = dict.fromkeys(columns, 0)
        game_data['title'] = title
        game_data['console'] = console
        game_data['esrb_rating'] = rating
        
        # Set 1 for descriptors that are found
        for descriptor in descriptor_list:
            # Normalize descriptor: replace spaces with underscores and convert to lowercase
            descriptor_normalized = descriptor.lower().replace(" ", "_")
            # print(f"Processing descriptor: {descriptor_normalized}")

            if descriptor_normalized  in descriptor_mapping.values():
                # Find the correct key in descriptor_mapping
                for key, value in descriptor_mapping.items():
                    if value == descriptor_normalized:
                        game_data[value] = 1
                        # print(f"Updated game data for descriptor: {key}")
        # print(game_data)
        data.append(game_data)
    
    # Save to CSV after scraping each page
    save_to_csv()

# Function to save the data to CSV
def save_to_csv():
    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_filename)
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # Append to the CSV file
    df.to_csv(csv_filename, mode='a', header=not file_exists, index=False)
    
    # Clear the data list after saving
    data.clear()
    print(f"Data saved to {csv_filename}")

# Loop through pages and scrape data
while True:
    # Scrape the current page
    scrape_page()

    # Check if there is a "Next" button and if it's enabled
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')  # Modify selector as needed
        if "disabled" in next_button.get_attribute('class'):  # Check if "Next" button is disabled
            break
        else:
            next_button.click()  # Click to go to the next page
            time.sleep(5)  # Give the page time to load
    except:
        # If "Next" button is not found, stop pagination
        break

# Close the driver
driver.quit()
