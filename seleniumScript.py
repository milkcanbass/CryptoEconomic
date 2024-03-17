from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Variables for customization
search_term = "ETH"  # Change this to your desired search term
csv_file_name = f"{search_term.lower()}_articles_cnbc.csv"  # CSV file name based on the search term

# Initialize the WebDriver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Construct the CNBC search URL using the search term
base_url = f'https://www.cnbc.com/search/?query={search_term}&qsearchterm={search_term}'

# Navigate to the CNBC search URL
driver.get(base_url)

# Wait for the "Newest" button to be clickable and then click it
wait = WebDriverWait(driver, 10)
newest_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sortdate"]')))
newest_button.click()

# Wait for a moment to ensure the articles are sorted
time.sleep(5)

# Open the CSV file for writing and write the header row
with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Timestamp'])

    # Scroll to load more articles
    for _ in range(20):  # Adjust based on the number of scrolls needed
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)  # Wait for the page to load

    # Find the container that holds all the articles
    articles = driver.find_elements(By.XPATH, '//*[@id="searchcontainer"]/div')

    # Loop through each article container
    for article in articles:
        try:
            link = article.find_element(By.XPATH, './div/div[2]/div[2]/a').get_attribute('href')
            title_element = article.find_element(By.XPATH, './div/div[2]/div[2]/a/span')
            title = title_element.text.strip()
            timestamp = article.find_element(By.XPATH, './div/div[2]/span/span[2]').text.strip()

            # Write the title, link, and timestamp to the CSV file
            writer.writerow([title, link, timestamp])

        except Exception as e:
            print(f"An error occurred while processing an article: {e}")
            continue

# Close the WebDriver
driver.quit()

# Print completion message
print(f'Finished writing articles to {csv_file_name}')
