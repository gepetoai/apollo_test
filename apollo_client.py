import requests
import os
import dotenv
import json

import time
from db import SupabaseClient

dotenv.load_dotenv()

key = os.environ.get('APOLLO_KEY')

class Apollo:
    def __init__(self, key):
        self.key = key
        self.base_url = "https://api.apollo.io/api/v1/"

    def make_request(self, url, data, max_retries=10, backoff_factor=3, initial_delay=1):
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }
        retries = 0
        delay = initial_delay  # Initial delay in seconds

        while retries < max_retries:
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                return json.loads(response.text)
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limited
                    print(f"Rate limited. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= backoff_factor  # Increase delay for next retry
                    retries += 1
                else:
                    print(f"Request failed with status code {response.status_code}: {e}")
                    break  # Break the loop for non-rate limit errors
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break  # Break the loop for non-HTTP errors
        print("Max retries exceeded or critical error occurred.")
        return None

    def search_organizations(self, ranges, locations, keywords, page=1, per_page=100, q_organization_name = None):
        url = f"{self.base_url}mixed_companies/search"
        data = {
            "api_key": self.key,
            "page": page,
            "per_page": per_page,
            "organization_num_employees_ranges": ranges,
            "organization_locations": locations,
            "q_organization_keyword_tags": keywords,
            "q_organization_name": q_organization_name
        },
        return self.make_request(url, data)

    def search_people(self, page, per_page, organization_ids, person_titles):
        url = f"{self.base_url}mixed_people/search"
        data = {
            "api_key": self.key,
            "page": page,
            "per_page": per_page,
            "organization_ids": organization_ids,
            "person_titles": person_titles
        }
        return self.make_request(url, data)

    def enrich_person(self, person_id, first_name):
        url = f"{self.base_url}people/match"
        data = {
            "api_key": self.key,
            "id": person_id, 
            "first_name": first_name
        }
        return self.make_request(url, data)


def collect_data(ap, ranges, locations, keywords, cap, person_titles):
    org_page = 1
    results = []

    while True:
        org_response = ap.search_organizations(ranges, locations, keywords, org_page, 100)
        if not org_response or 'organizations' not in org_response:
            break

        for org in org_response['organizations']:
            people_page = 1
            while True:
                people_response = ap.search_people(people_page, 100, [org['id']], person_titles)
                if not people_response or 'people' not in people_response:
                    break

                for person in people_response['people']:
                    results.append({
                        'organization_id': org['id'],
                        'organization_name': org['name'],
                        'organization_website': org['website_url'],
                        'person_id': person['id'],
                        'person_first_name': person['first_name'],
                        'person_last_name': person['last_name'],
                        'person_linkedin': person['linkedin_url'],
                        'person_email': person['email'] if person['email'] != 'email_not_unlocked@domain.com' else None,
                        'person_title': person['title']
                    })
                    if not results[-1]['person_email']:
                        enrichment = ap.enrich_person(person['id'], person['first_name'])

                        if enrichment and enrichment.get('person') is not None:
                            results[-1]['person_email'] = enrichment['person']['email']
                            results[-1]['person_linkedin'] = enrichment['person'].get('linkedin_url', results[-1]['person_linkedin'])

                    #remove the latest entry from results if there's no email address
                    if not results[-1]['person_email'] or results[-1]['person_email'] == '':
                        results.pop()

                    if len(results) >= cap:
                        print('hit cap!')
                        return results
                    
                if people_page >= people_response['pagination']['total_pages']:
                    break
                people_page += 1

        if org_page >= org_response['pagination']['total_pages']:
            break
        org_page += 1

    return results

