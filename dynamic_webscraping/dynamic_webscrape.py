from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

# Output file must be in same folder as script or have its path
    # If the Excel file already has a sheet named "webscraped" there will be an error (!)
excel_output_file = "INSERT_EXCEL_OUTPUT_FILE_NAME_HERE.xlsx"

#Link to be scraped
scrape_link = "INSERT_LINK_HERE"

# Delay between the scraping of each link in seconds
delay_between_link = 2

options = Options()
# Add your User-Agent
options.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1')


# --------------------------------------------------

# Make sure the webdriver executable is in your PATH
driver = webdriver.Firefox(options=options)

driver.get(scrape_link)

list_items = driver.find_elements(By.CSS_SELECTOR, 'MODIFY')

# Initialize empty lists to store the data
names = []
scrape_urls = []

# Iterate over the list items and extract the name and URL
for item in list_items:

    name_element = item.find_element(By.CSS_SELECTOR, 'MODIFY')
    name = name_element.text
    names.append(name)

    # Extract the URL from the anchor element
    scrape_url = name_element.get_attribute('MODIFY')
    scrape_urls.append(scrape_url)

# Create a DataFrame from the extracted data
data = {'Name': names, 'Scrape Urls': scrape_urls}
df = pd.DataFrame(data)

driver.quit()

# Print the DataFrame
print("All links that will be scraped:")
print("--------------------------------")
print(df)

df2 = pd.DataFrame(
    columns=['MODIFY', 'MODIFY'])


def scrape_url_func(url):
    global df2
    options = Options()
    options.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1')

    # Make sure the webdriver executable is in your PATH
    driver = webdriver.Firefox(options=options)

    driver.get(url)


    # Append the data as a new row to the DataFrame
    new_row = {'MODIFY':'MODIFY'}
    df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)

    driver.quit()


iterations = 0
for index, row in df.iterrows():
    if iterations > 5:
        break
    url = row['Scrape URL']
    print(f"Scraping {url} ...")
    scrape_url_func(url)
    print(f"Sleeping {delay_between_link} sec...")
    time.sleep(delay_between_link)
    iterations += 1


print("Final")
print(df2)

# Write DataFrame to Excel
with pd.ExcelWriter(excel_output_file, engine='openpyxl', mode='a') as writer:
    print("\nWriting to excel file...")
    df2.to_excel(writer, sheet_name='webscraped')  # Add your sheet name

print("Writing finished. Excel file saved.")
