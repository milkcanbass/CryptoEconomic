from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Initialize the WebDriver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

base_url = 'https://www.coindesk.com/search?s=ETH&sd=1609552284000&ed=1609552284000&df=Custom&i={}'

csv_file = 'articles.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])

    for page in range(0, 2):  # Adjust the range as needed
        url = base_url.format(page)
        driver.get(url)
        time.sleep(5)  # Adjust the sleep time as necessary

        # Find all the <a> tags with the specific class that contains the articles
        article_links = driver.find_elements(By.CSS_SELECTOR, 'a.searchstyles__ImageContainer-sc-ci5zlg-7')

        for article_link in article_links:
            img_tag = article_link.find_element(By.TAG_NAME, 'img')
            title = img_tag.get_attribute('alt')
            link = article_link.get_attribute('href')

            # Skip entries with undesired titles or links
            if title == "Logo of ETH" or '/price/' in link:
                continue

            # Construct the full URL if necessary
            if not link.startswith('http'):
                link = 'https://www.coindesk.com' + link

            writer.writerow([title, link])

        print(f'Finished page {page + 1}')

driver.quit()
print(f'Finished writing articles to {csv_file}')
