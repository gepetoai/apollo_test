from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_indeed(url):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Create a new Chrome WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)

    # Load the Indeed.com URL
    driver.get(url)

    # Get the page source after JavaScript has been executed
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Create a BeautifulSoup object with the page source
    soup = BeautifulSoup(page_source, "html.parser")

    # Return the parsed HTML
    return soup

# Example usage
url = "https://www.indeed.com/jobs?q=sales+development+representative&l=United+States&start=10"
indeed_html = scrape_indeed(url)
print(indeed_html.prettify())