import random,string

'''
generate creates a random new key dictionary from lowercase letters.
input:
    key_name, name of the key that would be generated.
outputs:
    tuple with a key_name and the dictionary that generated.
'''
def generate(key_name):
    key_dict = {}
    letters = string.ascii_lowercase
    letters_list = list(letters)
    random.shuffle(letters_list)
    shuffled = ''.join(letters_list)
    map = {letters[i]: shuffled[i] for i in range(len(letters))}
    key_dict[key_name] = map
    print(f'A new key called {key_name} was created')
    return key_name, key_dict

'''
encrypt_decrypt reads a text file and encrypt/decrypt it denepds on the key_dict that passed.
Inputs:
    source:plain file to read letters from(use a file with lowercase letters)
    dest: encrypted file to be written to using the mapping of the dictionary.
    key_dict:lowercase letters keys to lowercase letters values.
Outputs:
    data(str):it has the source file data
    res(str);it has the data after using the dictionary mapping.
'''
def encrypt_decrypt(source, dest, key_dict):
    data = ''
    res = ''
    try:
        with open(source, 'r') as f1, open(dest, 'w') as f2:
            while True:
                c = f1.read(1)
                data += c
                if not c:
                    break
                val = key_dict[c]
                res += val
                f2.write(val)
    except FileNotFoundError:
        print('File does not exist')
    f1.close()
    f2.close()
    return data, res
