from Crypto.Cipher import AES
import base64


def encrypt_send(aes_key, msg, iv):
    enc_s = AES.new(aes_key, AES.MODE_CFB, iv)

    if type(msg) == bytes:
        cipher_text = enc_s.encrypt(msg)
    else:
        cipher_text = enc_s.encrypt(msg.encode("utf-8"))

    encoded_cipher_text = base64.b64encode(cipher_text)
    return encoded_cipher_text


def decrypt_recv(aes_key, cipher, iv):

    try:
        decryption_suite = AES.new(aes_key, AES.MODE_CFB, iv)
        plain_text = decryption_suite.decrypt(base64.b64decode(cipher + b"=="))
        return (
            plain_text
            if type(plain_text) == str
            else plain_text.decode("utf-8", "ignore")
        )

    except TypeError:
        pass
