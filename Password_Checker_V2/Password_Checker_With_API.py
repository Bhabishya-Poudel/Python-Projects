import requests
import hashlib
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def check_password(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper() #Converts the password into a byte and then hashes it using SHA
#and finally converts to hexadecimal characters.
    password_first5 , password_tail = sha1_password[:5] , sha1_password[5:] 
#Only first 5 characters needed for passing into API documentation. Also store next characters for records.
    response = call_pwned_api(password_first5) 
#Calling the API
    return leaks_from_response(response, password_tail)


def call_pwned_api(password_first5):
    url = "https://api.pwnedpasswords.com/range/" + password_first5
    response = requests.get(url) #Sends the url to the API 
    if response.status_code != 200: #The API sends HTTP responsecode / status_code. 
        raise RuntimeError(f"The response error code is: {response.status_code}")
    return response #If no error, record the response for further calculation.


def leaks_from_response(response, password_tail):
    response_hashes = (line.split(':') for line in response.text.splitlines())
#Each response is split into lines and then into the hexdecimal value and cont value. 
    for response_hash, count in response_hashes:
        if response_hash == password_tail:
            return int(count)
    return 0
    

def main(arg):
    for password in arg:
        count = check_password(password)
        if count:
            print(f"{password} was found {count} times.")
        else:
            print(f"Requested password: {password} was not found.")

if __name__ == '__main__':
    use_env = sys.argv[1]
    if use_env == 'True':
        passwords = os.environ.get('Passwords').split(',')
        main(passwords)
    elif use_env == 'False':
        main(sys.argv[2:])
    else:
        raise RuntimeError('Invalid first argument, True or False required.')
