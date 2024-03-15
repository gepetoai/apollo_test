
import requests

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response was an unsuccessful status code.
        return response.text  # Returns the HTML content of the page.
    except requests.RequestException as e:
        return f"An error occurred: {e}"



