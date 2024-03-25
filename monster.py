from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


with open('monster_search2.html', 'r') as file:
    html_content = file.read()


def get_job_data(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the job opening elements
    job_elements = soup.select('article[data-testid="svx_jobCard"]')

    # Initialize an empty list to store job data
    job_data = []

    # Extract job details from each job element
    for job_element in job_elements:
        print(job_element)
        continue
        # Extract job title and URL
        job_title_element = job_element.select_one('h3[aria-label] a')
        job_title = job_title_element.get_text(strip=True)
        #format_job_title to remove all newlines and ensure only one space between words
        job_title = ' '.join(job_title.split())

        job_url = job_title_element['href']
        
        # Extract company name
        company_name = job_element.select_one('span[data-testid="company"]').get_text(strip=True)
        
        # Extract job location
        job_location = job_element.select_one('span[data-testid="jobDetailLocation"]').get_text(strip=True)
        
        # Extract job posting date
        job_date = job_element.select_one('span[data-testid="jobDetailDateRecency"]').get_text(strip=True)
        #example values of job_date are 'Today', '2 days', '9 days', '30+'
        #reformat job_date into a timestamptz object using the current date. three cases are "Today', X days', '30+ days'
        if job_date == 'Today':
            job_date = pd.to_datetime('today').strftime('%Y-%m-%d')
        elif 'days' in job_date and '+' not in job_date:
            days = int(job_date.split()[0])
            job_date = pd.to_datetime('today') - pd.DateOffset(days=days)
            job_date = job_date.strftime('%Y-%m-%d')
        else:
            job_date = pd.to_datetime('today') - pd.DateOffset(days=30)
            job_date = job_date.strftime('%Y-%m-%d')
            
        # Append job data to the list
        job_data.append([job_title, company_name, job_location, job_date, job_url])

    # Create a pandas DataFrame from the job data
    #df = pd.DataFrame(job_data, columns=['Job Title', 'Company', 'Location', 'Date', 'URL'])

    #return df

# Get job data from the HTML content
job_data = get_job_data(html_content)
print(job_data)

