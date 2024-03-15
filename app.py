import json
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apollo_client import Apollo
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Define your request model
class SearchRequest(BaseModel):
    ranges: List[str]
    locations: List[str]
    keywords: List[str]

# Instantiate the Apollo client with your key
key = os.getenv("APOLLO_API_KEY")
ap = Apollo(key)

@app.post("/org_search")
def org_search(search_request: SearchRequest):
    try:
        current_page = 0
        total_pages = 1
        results = []

        while current_page < total_pages:
            response = ap.org_search(ranges=search_request.ranges, locations=search_request.locations,
                                     keywords=search_request.keywords, page=current_page + 1, per_page=100)
            response = json.loads(response)
            current_page = response['pagination']['page']
            total_pages = response['pagination']['total_pages']
            orgs = response['organizations']

            for org in orgs:
                result = {"ID": org['id'], "Name": org['name'], "Website": org['website_url']}
                results.append(result)

        return {'response': 200, 'entries': response['pagination']['total_entries'], 'content': results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# #test the endpoint function
# search_request = SearchRequest(ranges=["500,5000"], locations=["United States", "Canada"], keywords=["logistics", "shipping"])
# test = org_search(search_request)['entries']
# print(test)