from apollo_client import collect_data, Apollo
from db import SupabaseClient
import streamlit
from dotenv import load_dotenv
import openai
import os
import ast 

load_dotenv()

sb = SupabaseClient(os.environ.get('SB_URL'), os.environ.get('SB_KEY'))
ap = Apollo(os.environ.get('APOLLO_KEY'))
openai = openai.OpenAI(api_key = os.environ.get('OPENAI_KEY'), max_retries = 5)

#used for function calling
def find_leads(headcount_range: list, locations: list, keywords: list, cap: int):
    results = collect_data(ap, headcount_range, locations, keywords, cap, ["CEO", "Chief Executive Officer", "CMO", "CRO", "Chief Marketing Officer", "Chief Revenue Officer", "SVP Sales", "SVP Marketing", "VP Sales", "VP Marketing", "VP Growth", "Senior Vice President Sales", "Senior Vice President Marketing", "Vice President Sales", "Vice President Marketing", "Vice President Growth"])

    added_results = []
    for result in results:
        try:
            if result['person_email']:
                sb.insert("leads", result)
                added_results.append(result)
        except Exception as e:
            print(e, ' for ', result)

    return {"leads added to database": len(added_results)}

#used for function calling
def schedule_campaign():
    return True

#tools
tools = [
  {
    "type": "function",
    "function": {
        "name": "find_leads",
        "description": "Searches for leads using three inputs: headcount_range, locations, keywords.",
        "parameters": {
            "type": "object",
            "properties": {
            "headcount_range": {
                "type": "array",
                "items": {
                "type": "string"
                },
                "description": "List of strings for the number of employees, e.g., ['1,10', '11,50']. To keep things simple unless otherwise specified, just use one range ex. ['100,10000']"
            },
            "locations": {
                "type": "array",
                "items": {
                "type": "string"
                },
                "description": "List of organization locations, e.g., ['United States', 'Canada']."
            },
            "keywords": {
                "type": "array",
                "items": {
                "type": "string"
                },
                "description": "List of keywords related to the organization, e.g., ['Legal', 'Law']."
            },
            "cap": {
                "type": "integer",
                "description": "Hard cap of how many lead records to retrieve. Default to 10 unless otherwise specified."
            }
            },
            "required": [
            "headcount_range",
            "locations",
            "keywords",
            "cap"
            ]
        }
    }
  },
    {
        "type": "function",
        "function": {
            "name": "schedule_campaign",
            "description": "Schedules the outbound sales campaign for the week. Takes no parameters",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]
prompt = '''
You are Alan, a sales agent who works for Gepeto, a tech startup that creates AI-powered autonomous sales agents. You lead all outbound sales efforts using the Apollo API, which provides demographic data for sales leads. 

You are talking to either Uzair, the CTO, or Mert, the CEO. 

STEP 1:  Get inputs
As your first message unless otherwise specified, clarify what kinds of organizations we want to target in this week's outbound campaign and use the find_leads function to do that search. To do this search, you need 3 things:

1. Company size: this is a headcount range, for example ['500, 5000'] for a range from 500 to 5000 employees.
2. Locations: a list of locations, for example ["United States", "Canada", "UK"]
3. Keywords for industries. For example, if we say HR software companies, you could use ["HR Technology", "HR SaaS", "HR Tech"]. But not ["HR", "Tech"] because that would also return all results for Tech. 
4. cap. This is the maximum number of leads to retrieve. Default to 10 unless otherwise specified.
example message: 
"Let's find you some leads. I need a company headcount range, locations, industry keywords, and a hard cap (default is 10)"
You do this in your first message

STEP 2: CONFIRM INPUTS
Before calling the function, confirm with us what inputs you are going to use for the call. 

STEP 3: CALL THE FUNCTION
Once the user confirm it, call the function. If there was an error, let us know and try again upon confirmation. 

STEP 4: SHARE LEAD COUNT
Once you call the function, let us know if the function call was successful and if so, how many leads were added to the Supabase database. 

STEP 5: ASK US TO REVIEW SUPABASE FOR CONFIRMATION
In the same message as above, ask us to login to supabase and review the leads before we schedule the outbound campaign. 

ex "134 leads added. Please review Supabase and confirm."

STEP 6: CONFIRM IF WE SHOULD SCHEDULE THE WEEK'S CAMPAIGN
Ask if we should schedule the week's campaign. ex "Should I proceed with campaign scheduling?"

STPE 7: SCHEDULE THE WEEK'S CAMPAIGN
Once we clearly confirm that we've reviewed Supabase and want to schedule the outbound campaign, call the schedule_campaign() function to schedule the campaign. 

STEP 8: CONFIRM SCHEDULING
Finally, confirmed the campaign has been scheduled. If there was an error, let us know and try again upon confirmation. 

ex "134 initial emails confirmed scheduled."

TONE
Keep all your answers as concise and brief as possible. Literally use the fewest words possible.
If the user requests anything that's not possible, politely let them know you can't do it. 
If the user asks anything out of scope from this prompt, let them know it's out of scope.
'''

#ChatCompletions API
def generate_response(all_messages, max_tokens = 250, tools = tools, prompt = prompt):
    messages = [{"role": "system", "content": prompt}]
    messages = messages + all_messages

    #generate response
    print(all_messages)
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
        return completion.choices[0].message.content

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
        
        #generate response
        completion = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature = 0,
            tools=tools,
            tool_choice="auto"
            )

        #and return it
        return completion.choices[0].message.content
    

test_messages = [{"role": "assistant", "content": "Let's find some leads. I need a company headcount range, locations, industry keywords, and a hard cap (default is 10)."}]
test_messages.append({"role": "user", "content": "['100,10000'], ['United States', 'Canada'], ['Legal', 'Law'], 10"})
print(generate_response(test_messages))