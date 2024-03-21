import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import openai
import os
import ast
from dotenv import load_dotenv

load_dotenv()

openai = openai.OpenAI(api_key = os.environ.get('OPENAI_KEY'), max_retries = 5)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse, urljoin

def fetch_url_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script, style, and other non-content tags
        for script_or_style in soup(["script", "style", "header", "footer", "nav", "noscript"]):
            script_or_style.decompose()

        # Remove comment nodes
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # Extract coherent and readable text content
        text_blocks = soup.stripped_strings
        all_text = ' '.join(filter(lambda x: len(x.split()) > 3, text_blocks))  # Filter out very short text fragments

        # Extract URLs
        parsed_url = urlparse(url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        urls = set()

        for link in soup.find_all('a', href=True):
            href = link['href']
            joined_url = urljoin(base_domain, href)
            parsed_href = urlparse(joined_url)
            if parsed_href.netloc == parsed_url.netloc:
                urls.add(joined_url)

        # Extract and enhance form details
        forms = []
        for form in soup.find_all('form'):
            form_details = {
                'action': urljoin(base_domain, form.get('action', '')),
                'method': form.get('method', 'get').lower(),
                'inputs': []
            }

            for input_tag in form.find_all('input'):
                input_details = {
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name'),
                    'value': input_tag.get('value', ''),
                    'label': ''
                }
                # Attempt to find the input's label
                if input_tag.get('id'):
                    label = form.find('label', {'for': input_tag.get('id')})
                    if label:
                        input_details['label'] = label.get_text(strip=True)
                form_details['inputs'].append(input_details)

            forms.append(form_details)

        return {
            'urls': list(urls),
            'form_details': forms,
            'text': all_text  # Coherent and readable text content
        }
    except requests.RequestException as e:
        return {'error': str(e)}




tools = [
  {
    "type": "function",
    "function": {
        "name": "fetch_url_data",
        "description": "Taking a url as an input, it fetches the readable text, url links, and form details (if any) present in the url.",
        "parameters": {
            "type": "object",
            "properties": {
            "url": {
                "type": "string",
                "description": "A string representing the URL of the page to fetch information about."
                }
            },
            "required": [
            "url"
            ]
        }
    }
  }
]

prompt1 = '''
Your job is to crawl a website until you find a a URL with an interest form of some kind, designed as a lead funnel for customers. 
You can use the fetch_url_data function to get the readable text content and links from a given URL. 
You can keep calling the function until you've found it, but only scan each webpage one.'''

prompt2 = '''
Your job is to crawl a website to understand what this business does and search for pricing information. 
Our goal is to figure out, using basic assumptions if necessary, how much this business makes in revenue per customer per year.
The fetch_url_data function can be used to get the HTML content from a given URL as well as embedded links for further exploration.
You can keep calling the function until you've found it, but only scan each webpage once.'''


#ChatCompletions API
def generate_response(all_messages, max_tokens = 250, tools = tools, prompt = prompt2):
    messages = [{"role": "system", "content": prompt}]
    messages = messages + all_messages

    #generate response
    completion = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature = 0,
        tools=tools,
        max_tokens = max_tokens,
        tool_choice="auto"
        )
    
    #if content is generated, return it
    if completion.choices[0].message.content:
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})

    #if a function call is returned execute it...
    elif len(completion.choices[0].message.tool_calls) > 0:
        tool_calls = completion.choices[0].message.tool_calls
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            tool_id = tool_call.id
            arguments = tool_call.function.arguments
            arguments = ast.literal_eval(arguments)

            output = eval(function_name)(**arguments)
            messages.append({"role": "function", "tool_call_id": tool_id, "name": function_name, "content": str(output)})
        
    return messages[1:]


messages=[{'role': 'user', 'content': 'use https://www.hubspot.com/'}]


user_input = ""
while user_input != "exit":
    messages = generate_response(messages)
    print(f"{messages[-1]['role']}: {messages[-1]['content']}\n") 

    if messages[-1]['role'] == "assistant":
        user_input = input("You: ")
        messages.append({"role": "user", "content": user_input})
        print(f"{messages[-1]['role']}: {messages[-1]['content']}\n") 


# test = fetch_url_data('https://www.hubspot.com/')
# print(test)