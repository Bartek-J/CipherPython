import glob, os

from datetime import datetime
from Crypto.Cipher import ChaCha20, Salsa20, ARC4
from Crypto.Random import get_random_bytes
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter

def entropy(string):
    freq_dict = dict(Counter(string))
    entropy_val = 0
    total_chars = len(string)

    for char in freq_dict:
        probability = freq_dict[char] / total_chars
        entropy_val += probability * math.log2(probability)
    return -entropy_val

def get_text_from_file(file_name) -> str:
    file = open(file_name, mode='r', encoding='utf8')
    text = file.read()
    file.close()
    return text


def encrypt_text(text: str, cipher, name: str) -> None:
    print(f'Encrypting {name}')
    start_time = datetime.now()
    encrypted_text = cipher.encrypt(bytes(text, encoding='utf-8'))
    return (datetime.now() - start_time).total_seconds()

def make_plot(plot_data1, plot_data2, plot_data3) -> None:
    files_length = plot_data1.pop('file_length')
    odstepy_x = np.linspace(0, len(files_length) - 1, len(files_length))
    #plt.figure(1)
    fig,ax = plt.subplots()
    fig.suptitle('Niska entropia')
    for name, values in plot_data1.items():
        ax.plot(odstepy_x, values, marker='o', label=name, alpha=0.7, linestyle='-')

    ax.set_xticks(odstepy_x)
    ax.set_xticklabels(files_length)
    plt.legend()
    ax.set_title('Czas wykonania w zależności od rozmiaru pliku')
    ax.set_xlabel('Ilość znaków')
    ax.set_ylabel('Czas [s]')

    files_length = plot_data2.pop('file_length')
    odstepy_x = np.linspace(0, len(files_length) - 1, len(files_length))
    #plt.figure(2)
    fig,ax = plt.subplots()
    fig.suptitle('Średnia entropia')
    for name, values in plot_data2.items():
        ax.plot(odstepy_x, values, marker='o', label=name, alpha=0.7, linestyle='-')

    ax.set_xticks(odstepy_x)
    ax.set_xticklabels(files_length)
    plt.legend()
    ax.set_title('Czas wykonania w zależności od rozmiaru pliku')
    ax.set_xlabel('Ilość znaków')
    ax.set_ylabel('Czas [s]')

    files_length = plot_data3.pop('file_length')
    odstepy_x = np.linspace(0, len(files_length) - 1, len(files_length))
    #plt.figure(3)
    fig,ax = plt.subplots()
    fig.suptitle('Wysoka entropia')
    for name, values in plot_data3.items():
        ax.plot(odstepy_x, values, marker='o', label=name, alpha=0.7, linestyle='-')

    ax.set_xticks(odstepy_x)
    ax.set_xticklabels(files_length)
    plt.legend()
    ax.set_title('Czas wykonania w zależności od rozmiaru pliku')
    ax.set_xlabel('Ilość znaków')
    ax.set_ylabel('Czas [s]')

    plt.show()


def main() -> None:
    os.chdir("./pliki/Niska")
    texts_uns = {file: get_text_from_file(file) for file in glob.glob("*.txt")}
    texts = dict(sorted(texts_uns.items(), key=lambda item: len(item[1])))
    plot_data = {'file_length': [], 'RC4': [], 'Salsa': [], 'ChaCha': []}
    key16 = get_random_bytes(16)
    key32 = get_random_bytes(32)
    iv = get_random_bytes(8)

    for name, text in texts.items():
        file_len = len(text)
        print('---------------------------------')
        print(f'file: {name.split(".")[0]}')
        print(f'Text length: {file_len}')
        print(f'entropia: {entropy(text)}')
        plot_data['file_length'].append(file_len)
        plot_data['RC4'].append(encrypt_text(text, ARC4.new(key16), 'RC4'))
        plot_data['Salsa'].append(encrypt_text(text, Salsa20.new(key16, iv), 'Salsa'))
        plot_data['ChaCha'].append(encrypt_text(text, ChaCha20.new(key=key32, nonce=iv), 'ChaCha'))

    os.chdir("..")
    os.chdir("./Srednia")
    texts_uns2 = {file: get_text_from_file(file) for file in glob.glob("*.txt")}
    texts2 = dict(sorted(texts_uns2.items(), key=lambda item: len(item[1])))
    plot_data2 = {'file_length': [], 'RC4': [], 'Salsa': [], 'ChaCha': []}

    for name, text in texts2.items():
        file_len2 = len(text)
        print('---------------------------------')
        print(f'file: {name.split(".")[0]}')
        print(f'Text length: {file_len2}')
        print(f'entropia: {entropy(text)}')
        plot_data2['file_length'].append(file_len2)
        plot_data2['RC4'].append(encrypt_text(text, ARC4.new(key16), 'RC4'))
        plot_data2['Salsa'].append(encrypt_text(text, Salsa20.new(key16, iv), 'Salsa'))
        plot_data2['ChaCha'].append(encrypt_text(text, ChaCha20.new(key=key32, nonce=iv), 'ChaCha'))

    os.chdir("..")
    os.chdir("./Wysoka")
    texts_uns3 = {file: get_text_from_file(file) for file in glob.glob("*.txt")}
    texts3 = dict(sorted(texts_uns3.items(), key=lambda item: len(item[1])))
    plot_data3 = {'file_length': [], 'RC4': [], 'Salsa': [], 'ChaCha': []}

    for name, text in texts3.items():
        file_len3 = len(text)
        print('---------------------------------')
        print(f'file: {name.split(".")[0]}')
        print(f'Text length: {file_len3}')
        print(f'entropia: {entropy(text)}')
        plot_data3['file_length'].append(file_len3)
        plot_data3['RC4'].append(encrypt_text(text, ARC4.new(key16), 'RC4'))
        plot_data3['Salsa'].append(encrypt_text(text, Salsa20.new(key16, iv), 'Salsa'))
        plot_data3['ChaCha'].append(encrypt_text(text, ChaCha20.new(key=key32, nonce=iv), 'ChaCha'))


    make_plot(plot_data, plot_data2, plot_data3)

main()
