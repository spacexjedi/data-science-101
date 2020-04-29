'''
Challenge Codenation
'''
import string
import json
import hashlib


plain = string.ascii_letters # alphabet
shift = int(input('Shift by: ')) # Enter the rotation 
message = input('Encrypt: ') # Message user want's to ecrypt
print() 


def encrypt_message(shift, message): # function that generates the encrypted message based on shift input
    encrypt_message = ''

    for letter in message:
        i = (plain.index(letter) + shift) % 52
        encrypt_message += plain[i] # set encrypted message equal to the rotation

    return 'Encrypted message: {}'.format(encrypt_message)


def decrypt_message(shift, encrypt): # function decrypts the encrypted message
    decrypted_message = ''

    for letter in encrypt:
        try:
            i = (plain.index(letter) - shift) % 52
            decrypted_message += plain[i]
        except ValueError: # added Value error because there was a value error
            decrypted_message += letter

    return 'Decrypted: {}'.format(decrypted_message)

encrypted = encrypt_message(shift, message)
print(encrypted)

decrypted = decrypt_message(shift, encrypted)
print(decrypted)


data = {
    "cypher": {
        "numero_casas": 10,
	    "token":"d56324627901796970ac5209829be865ab88ea30",
	    "cifrado": encrypted,
	    "decifrado": decrypted,
	    "resumo_criptografico": "aqui vai o resumo"
    }
}

with open("answer.json", "w") as write_file:
    json.dump(data, write_file)

print(data)

newdata = hashlib.sha256()
newdata.update(decrypted)
newdata.digest()

data = {
    "cypher": {
        "numero_casas": 10,
	    "token":"d56324627901796970ac5209829be865ab88ea30",
	    "cifrado": encrypted,
	    "decifrado": decrypted,
	    "resumo_criptografico": newdata
    }
}

with open("answer.json", "w") as write_file:
    json.dump(data, write_file)

print("Final combat\n")
print(data)
