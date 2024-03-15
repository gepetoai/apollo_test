import requests
import os
import dotenv
import json
import csv
import time

dotenv.load_dotenv()

key = os.environ.get('APOLLO_KEY')

class Apollo:
    def __init__(self, key):
        self.key = key
        self.base_url = "https://api.apollo.io/api/v1/"

    def make_request(self, url, data):
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def search_organizations(self, ranges, locations, keywords, page=1, per_page=100):
        url = f"{self.base_url}mixed_companies/search"
        data = {
            "api_key": self.key,
            "page": page,
            "per_page": per_page,
            "organization_num_employees_ranges": ranges,
            "organization_locations": locations,
            "q_organization_keyword_tags": keywords
        }
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

def collect_data(ap, ranges, locations, keywords, person_titles):
    page = 1
    results = []

    while True:
        time.sleep(2)
        org_response = ap.search_organizations(ranges, locations, keywords, page, 100)
        if not org_response or 'organizations' not in org_response:
            break

        for org in org_response['organizations']:
            time.sleep(2)
            people_response = ap.search_people(1, 100, [org['id']], person_titles)
            if not people_response or 'people' not in people_response:
                continue

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

                # if not results[-1]['person_email']:
                #     enrichment = ap.enrich_person(person['id'], person['first_name'])
                #     if enrichment and 'matches' in enrichment and len(enrichment['matches']) > 0:
                #         results[-1]['person_email'] = enrichment['matches'][0]['email']

        if page >= org_response['pagination']['total_pages']:
            break
        page += 1

    return results

def save_to_csv(results, filename="output.csv"):
    keys = results[0].keys() if results else []
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

ap = Apollo(key)
results = collect_data(ap, ["500,1000"], ["USA"], ["logistics", "shipping"], ["CEO", "Chief Executive Officer", "CMO", "CRO", "Chief Marketing Officer", "Chief Revenue Officer", "SVP Sales", "SVP Marketing", "VP Sales", "VP Marketing", "VP Growth"])
save_to_csv(results)
