import math
import glob, os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

from datetime import datetime
from Crypto.Cipher import ChaCha20, Salsa20, ARC4
from Crypto.Random import get_random_bytes
from collections import Counter


class Szyfrowanie:
    def entropy(self, string):
        freq_dict = dict(Counter(string))
        entropy_val = 0
        total_chars = len(string)

        for char in freq_dict:
            probability = freq_dict[char] / total_chars
            entropy_val += probability * math.log2(probability)
        return -entropy_val

    def get_text_from_file(self, file_name) -> str:
        file = open(file_name, mode='r', encoding='utf8')
        text = file.read()
        file.close()
        return text


    def encrypt_text(self, text: str, cipher, name: str) -> None:
        start_time = datetime.now()
        encrypted_text = cipher.encrypt(bytes(text, encoding='utf-8'))
        time_taken = (datetime.now() - start_time).total_seconds()
        self.listbox.insert(END, f'  Encrypting {name}')
        self.listbox.insert(END, f'  time: {time_taken}')
        return time_taken

    def make_plot(self, plot_data) -> None:
        files_length = plot_data.pop('file_length')
        odstepy_x = np.linspace(0, len(files_length) - 1, len(files_length))
        fig,ax = plt.subplots()
        for name, values in plot_data.items():
            ax.plot(odstepy_x, values, marker='o', label=name, alpha=0.7, linestyle='-')

        ax.set_xticks(odstepy_x)
        ax.set_xticklabels(files_length)
        plt.legend()
        ax.set_title('Czas wykonania w zależności od rozmiaru pliku')
        ax.set_xlabel('Ilość znaków')
        ax.set_ylabel('Czas [s]')
        plt.show()


    def main(self) -> None:
        self.window = Tk()
        self.window.option_add('*Font', '32')
        self.window.geometry("1000x1000")
        os.chdir("./pliki")
        texts_uns = {file: self.get_text_from_file(file) for file in glob.glob("*.txt")}
        texts = dict(sorted(texts_uns.items(), key=lambda item: len(item[1])))
        plot_data = {'file_length': [], 'RC4': [], 'Salsa': [], 'ChaCha': []}
        key16 = get_random_bytes(16)
        key32 = get_random_bytes(32)
        iv = get_random_bytes(8)
        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.window, font=("Arial", 16), height=1000, width=1000)
        self.listbox.pack(padx=100)
        self.listbox.insert(END, '  Tested files:')
        for name, text in texts.items():
            file_len = len(text)
            self.listbox.insert(END, '  ---------------------------------------')
            self.listbox.insert(END, f'  file: {name.split(".")[0]}')
            self.listbox.insert(END, f'  Text length: {file_len}')
            self.listbox.insert(END, f'  entropia: {self.entropy(text)}')
            plot_data['file_length'].append(file_len)
            plot_data['RC4'].append(self.encrypt_text(text, ARC4.new(key16), 'RC4'))
            plot_data['Salsa'].append(self.encrypt_text(text, Salsa20.new(key16, iv), 'Salsa'))
            plot_data['ChaCha'].append(self.encrypt_text(text, ChaCha20.new(key=key32, nonce=iv), 'ChaCha'))
        self.make_plot(plot_data)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.window.mainloop()


Szyfrowanie().main()
