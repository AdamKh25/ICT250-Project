import math


# encrypt message using transposition cipher
def encryptMessage(key, message):
    # create empty columns
    ciphertext = [''] * key

    # read message column by column
    for col in range(key):
        pointer = col
        while pointer < len(message):
            ciphertext[col] += message[pointer]
            pointer += key

    return ''.join(ciphertext)


# decrypt message using transposition cipher
def decryptMessage(key, message):
    # calculate grid dimensions
    numColumns = math.ceil(len(message) / key)
    numRows = key

    # calculate shaded boxes
    numShadedBoxes = (numColumns * numRows) - len(message)

    plaintext = [''] * numColumns
    col = row = 0

    # rebuild plaintext row by row
    for symbol in message:
        plaintext[col] += symbol
        col += 1

        # move to next row when needed
        if (col == numColumns) or (col == numColumns - 1 and row >= numRows - numShadedBoxes):
            col = 0
            row += 1

    return ''.join(plaintext)


# wrapper for encryption
def encrypt(text, key):
    return encryptMessage(key, text)

# wrapper for decryption
def decrypt(text, key):
    return decryptMessage(key, text)
