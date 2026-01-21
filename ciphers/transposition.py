import math

def encryptMessage(key, message):
    # write down the message in rows; read off column by column
    ciphertext = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(message):
            ciphertext[col] += message[pointer]
            pointer += key
    return ''.join(ciphertext)

def decryptMessage(key, message):
    numColumns = math.ceil(len(message) / key)
    numRows = key
    numShadedBoxes = (numColumns * numRows) - len(message)
    plaintext = [''] * numColumns
    col = row = 0
    for symbol in message:
        plaintext[col] += symbol
        col += 1
        if (col == numColumns) or (col == numColumns - 1 and row >= numRows - numShadedBoxes):
            col = 0
            row += 1
    return ''.join(plaintext)

def encrypt(text, key): return encryptMessage(key, text)
def decrypt(text, key): return decryptMessage(key, text)
