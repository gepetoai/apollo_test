from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Import Service

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Path to chromedriver executable
chrome_service = Service(executable_path='/path/to/chromedriver')  # Use the Service object

# Set up driver with the Service object
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Go to the webpage
driver.get("http://hellogepeto.com")

# Get the dimensions of the entire page
total_width = driver.execute_script("return document.body.offsetWidth")
total_height = driver.execute_script("return document.body.scrollHeight")

# Resize the window to the entire page
driver.set_window_size(total_width, total_height)

# Take the screenshot of the entire page
driver.save_screenshot("full_website_screenshot.png")

# Clean up (close the browser)
driver.quit()
