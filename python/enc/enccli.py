import enc_dec,json

def enc_init():
    commands = {
        'info': info,
        'load': load,
        'newkey': newkey,
        'save': save,
        'enc': enc_or_dec,
        'dec': enc_or_dec}
    return commands


def main_cli():
    state = 'not saved'
    current_key_name, enc_text, dec_text, enc_mapped, dec_mapped = '', '', '', '', ''
    key_dict = {}
    commands = enc_init()
    cli_end = False
    while not cli_end:
        cmd_str = input('subs>')
        cmd = cmd_str.split()
        if cmd and cmd[0] == 'done':
            cli_end = True
        if cmd:
            if cmd[0] == 'info':
                ret = commands[cmd[0]](current_key_name, state, enc_text, dec_text, enc_mapped, dec_mapped)
            if cmd[0] == 'save':
                ret = commands[cmd[0]](cmd[1:], key_dict)
                state = 'saved' if ret else 'not saved'

            if cmd[0] == 'newkey' or cmd[0] == 'load':
                ret = commands[cmd[0]](cmd[1:])
                current_key_name = ret[0]
                key_dict = ret[1].copy()
                state='not saved' if cmd[0]=='newkey' else 'saved'

            if cmd[0] == 'enc' or cmd[0] == 'dec':
                ret = commands[cmd[0]](
                    cmd[1:], key_dict, current_key_name, mode=cmd[0])

                if cmd[0]=='enc':
                    enc_text = ret[0]
                    enc_mapped = ret[1]
                else:
                    dec_text = ret[0]
                    dec_mapped = ret[1]

#loads a file that contain key name and it's lowercase to lowercase letters dictionary. 
def load(file_name):
    file_name = ''.join(file_name)
    try:
        with open(file_name, 'r') as f:
            key_dict = json.load(f)
    except FileNotFoundError:
        print('file does not exist!')

    keys_list = list(key_dict.keys())
    current_key_name = keys_list[0]
    f.close()
    return current_key_name, key_dict

#saving a file as a json format,returns true when success.
def save(file_name, key):
    if not key:
        print('No key to save,Please generate a key first')
        return False

    file_name = ''.join(file_name)
    try:
        with open(file_name, 'w') as f:
            json.dump(key, f, indent=2)
            print(f'Enc/Dec keys saved in {file_name} file')
    except FileNotFoundError:
        print(f"{file_name} not exist")

    f.close()
    return True


def newkey(key_name):
    key_dict = {}
    key_name = key_name[0]
    key_dict = enc_dec.generate(key_name) #calls other module to generate a new key.
    return key_dict

'''
enc_or_dec makes encryption/decryption to a file depends on the mode that passed.
Inputs:
    files:list of source and destination file.
    key_dict:lowercase to lowercase mapped letters.
    key_name:name of the key currently used for decryption/encryption.
    mode:keyword argument used to choose what operation to make,
        choose only one of two operations: "enc" or "dec".
Output:
    reutrns the data before and after encryption/decryption.        
'''
def enc_or_dec(files, key_dict, key_name, *, mode):
    source = files[0]
    dest = files[1]
    enc_dec_dict = key_dict[key_name]
    inv_enc_dec_dict = {v: k for k, v in enc_dec_dict.items()}
    if mode == 'enc':
        ret = enc_dec.encrypt_decrypt(source, dest, enc_dec_dict)
        print(f"File {source} was encrypted into {dest} ")

    if mode == 'dec':
        ret = enc_dec.encrypt_decrypt(source, dest, inv_enc_dec_dict)
        print(f"File {source} was decrypted into {dest} ")
    return ret

#printing the current status of the enc/dec operation and IO operations.
def info(current_key, state, enc_text, dec_text, enc_mapped, dec_mapped):
    print(f'Current key:{current_key}\nstate:{state}')
    print(f'Encryption:\n{enc_text}\n{enc_mapped}')
    print(f'Decryption:\n{dec_text}\n{dec_mapped}')


#main program starts here...
main_cli()
