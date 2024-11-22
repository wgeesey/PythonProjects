##### Password Checker ####

# K-anonymity: This concept ensures that a given piece of data (such as a password) cannot be uniquely identified 
# from a dataset, even if it's part of a large dataset. The idea is to keep the data anonymous by comparing it 
# against a large pool of similar items (in this case, passwords that have been "pwned").

# Hash Function: A hash function takes an input (e.g., a password) and returns a fixed-length value (the hash). 
# The same input will always produce the same hash, but even a small change in the input will result in a 
# completely different hash. Hash functions are also case-sensitive, meaning 'password' and 'Password' will have 
# different hashes.

# Idempotent: An operation is considered idempotent if performing it multiple times results in the same effect 
# as performing it once. In the context of this code, the operation of checking a password against the "Pwned Passwords" API 
# is idempotent because querying the same password multiple times will return the same result.

import requests
import hashlib
import sys

# Function to request data from the Pwned Passwords API.
# query_char is the first 5 characters of the SHA-1 hash of the password.
def request_api_data(query_char):
    # Dynamically creates the URL for the API by appending the first 5 characters of the hashed password
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    
    # If the request is unsuccessful (anything other than status code 200), raise an error
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the pwned_api_check and try again')
    
    return res

# Function to count how many times a password hash has been "pwned" (found in data breaches)
# hashes is the response text from the API that contains a list of hashes and their counts.
def get_password_leaks_count(hashes, hash_to_check):
    # Each line in the API response is in the format 'hash:count'. Split each line by ':'.
    hashes = (line.split(':') for line in hashes.text.splitlines())
    
    # Check if the given hash (hash_to_check) exists in the response
    for h, count in hashes:
        if h == hash_to_check:
            return count  # If found, return the count of breaches for this hash
    return 0  # If not found, return 0

# Function to check a password against the Pwned Passwords API
# This function hashes the password, sends the first 5 characters to the API, and checks the response.
def pwned_api_check(password):
    # Convert password to SHA-1 hash and get the first 5 characters and the remaining tail
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    
    # Call the API with the first 5 characters of the hash
    response = request_api_data(first5_char)
    
    # Check the API response to see if the password (hash) has been pwned
    return get_password_leaks_count(response, tail)

# Main function to process the passwords passed as command-line arguments
def main(args):
    # Loop through each password provided as argument and check it
    for password in args:
        count = pwned_api_check(password)  # Check the password against the Pwned Passwords API
        if count:
            # If the password was found, print the number of times it was found in breaches
            print(f'{password} was found {count} times...you should probably change your password.')
        else:
            # If the password was not found, indicate that it's safe
            print(f'{password} was NOT found, carry on!')
    
    return 'done'

    ### The following code block is commented out because it is an alternative for handling input via stdin:
    # This approach can be used when running the script from the command line with redirected input (using <).
    # for /f "tokens=*" %a in (C:\Users\willi\Desktop\pwordtest.txt) do python checkmypassword.py %a
    # This approach uses sys.stdin to read passwords line by line.
    # for password in sys.stdin:
    #     password = password.strip()  # Remove any leading/trailing whitespace/newlines
    #     count = pwned_api_check(password)
    #     if count:
    #         print(f'{password} was found {count} times...you should probably change your password.')
    #     else:
    #         print(f'{password} was NOT found, carry on!')
    # return 'done!'

# Entry point to run the script, passing command-line arguments
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
