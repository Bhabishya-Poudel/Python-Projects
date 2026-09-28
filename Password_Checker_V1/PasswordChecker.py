import string

password = "qWerty"

upper = any([1 if c in string.ascii_uppercase else 0 for c in password])
lower = any([1 if c in string.ascii_lowercase else 0 for c in password])
special = any([1 if c in string.punctuation else 0 for c in password])
digits = any([1 if c in string.digits else 0 for c in password])

characters = [upper, lower, special, digits]
length = len(password)

score = 0

with open('CommonPasswords.txt', 'r') as file:
    common = file.read().splitlines()
file.close()

if password in common:
    print("Try again, password found in a common list.")
    exit()
else:
    print("Keep Going")

if length > 7:
    score += 1
elif length > 9:
    score += 2
elif length >12:
    score += 3

print(f"Password length is str({length}), adding a score of str({score}).")

if sum(characters) > 1:
    score += 1
elif sum(characters) > 2:
    score += 2
else:
    score += 3

if score <4:
    print(f"The password is quite weak")
elif score <8:
    print(f"The password is OK!")
elif score <12:
    print(f"The password is great!")
elif score >15:
    print(f"Excellent!")



