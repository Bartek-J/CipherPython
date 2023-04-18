from datetime import datetime
from Crypto.Cipher import ChaCha20, Salsa20, ARC4
from Crypto.Random import get_random_bytes


FILES_TO_TEST = ['test_file.txt', 'test_file2.txt', 'test_file3.txt', 'pan_tadeusz.txt', 'lalka.txt', 'books.txt']


def get_text_from_file(file_name) -> str:
    file = open(file_name, mode='r', encoding='utf8')
    text = file.read()
    file.close()
    return text


def encrypt_text(text: str, cipher, name: str) -> None:
    print(f'Encrypting {name}')
    start_time = datetime.now()
    encrypted_text = cipher.encrypt(bytes(text, encoding='utf-8'))
    print(f'Time taken: {datetime.now() - start_time}')


def main() -> None:
    texts = {file: get_text_from_file(file) for file in FILES_TO_TEST}
    key16 = get_random_bytes(16)
    key32 = get_random_bytes(32)
    iv = get_random_bytes(8)

    for name, text in texts.items():
        print('---------------------------------')
        print(f'file: {name.split(".")[0]}')
        print(f'Text length: {len(text)}')
        encrypt_text(text, ARC4.new(key16), 'RC4')
        encrypt_text(text, Salsa20.new(key16, iv), 'Salsa')
        encrypt_text(text, ChaCha20.new(key=key32, nonce=iv), 'ChaCha')
main()
