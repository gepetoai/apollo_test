from bs4 import BeautifulSoup
import pandas as pd

#open monster_search.html and save it as html_content
with open('apollo_test/monster_search.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the job opening elements
job_elements = soup.select('article[data-testid="svx_jobCard"]')

# Initialize an empty list to store job data
job_data = []

# Extract job details from each job element
for job_element in job_elements:
    # Extract job title and URL
    job_title_element = job_element.select_one('h3[aria-label] a')
    job_title = job_title_element.get_text(strip=True)
    job_url = job_title_element['href']
    
    # Extract company name
    company_name = job_element.select_one('span[data-testid="company"]').get_text(strip=True)
    
    # Extract job location
    job_location = job_element.select_one('span[data-testid="jobDetailLocation"]').get_text(strip=True)
    
    # Extract job posting date
    job_date = job_element.select_one('span[data-testid="jobDetailDateRecency"]').get_text(strip=True)
    
    # Append job data to the list
    job_data.append([job_title, company_name, job_location, job_date, job_url])

# Create a pandas DataFrame from the job data
df = pd.DataFrame(job_data, columns=['Job Title', 'Company', 'Location', 'Date', 'URL'])

# Save as a CSV
df.to_csv('job_openings.csv', index=False)