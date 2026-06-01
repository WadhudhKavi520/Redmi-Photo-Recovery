import os
import filetype
from Crypto.Cipher import AES
from Crypto.Util import Counter

# Xiaomi's hardcoded IV - do not change
sAesIv = 22696201676385068962342234041843478898

# PASTE THE 32-CHAR OUTPUT FROM 'xxd' HERE
hex_key = "3082046c30820354a003020102020900" # Example key

# Convert the hex string directly to the 16-byte binary key
secretKey = bytes.fromhex(hex_key)

def decrypt_file(filename):
    with open(filename, 'rb') as file:
        counter = Counter.new(128, initial_value=sAesIv)
        aes = AES.new(secretKey, mode=AES.MODE_CTR, counter=counter)
        return aes.decrypt(file.read())

def main(path):
    for filename in os.listdir(path):
        if filename.endswith('.lsa'):
            filepath = os.path.join(path, filename)
            data = decrypt_file(filepath)
            
            # A successful JPEG starts with 0xFF 0xD8
            ext = filetype.guess_extension(data[:1024]) or 'jpg'
            outpath = os.path.join(path, f'SUCCESS_{os.path.splitext(filename)[0]}.{ext}')
            
            with open(outpath, 'wb') as file:
                file.write(data)
            print(f'Saved: {outpath}')

if __name__ == '__main__':
    main('.')