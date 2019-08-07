import os
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *
from src.sumPy import hash_file, get_hashsum
from hashlib import sha256
from nltk.tokenize import word_tokenize
import sys

class UserInterface:
    ''' This class defines the user interface of SumPy '''

    def __init__(self):
        ''' create a ui for SumPy'''
        self.root = tk.Tk();
        self.root.title()
        self.HEIGHT = 700
        self.WIDTH = 900
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.header = tk.Frame(self.canvas, bg='#2a1f6b')
        self.heading = tk.Text(self.header, font=('Lucida Console', 125), bg='#2a1f6b', bd=0, borderwidth=0, highlightthickness=0)
        
        self.frame = tk.Frame(self.canvas, bg='#2a1f6b')
        # make frame children to house inputs and output
        self.f1 = tk.Frame(self.frame, bg='red')
        self.f2 = tk.Frame(self.frame, bg='pink')
        self.f3 = tk.Button(self.frame, bg='purple')
        self.clickMessage = "click here to hash!\n" 
        self.clickMe = tk.Label(self.f3, bg='purple', text=self.clickMessage, font=('Lucida Console', 25), bd=0, highlightthickness=0, anchor="center")

        self.entry = tk.Entry(self.f1, font=('Lucida Console', 35), bg='green')
        self.entry2 = tk.Entry(self.f2, font=('Lucida Console', 35), bg='green')
        self.browse = tk.Button(self.f1, bg='orange', command=self.browse_files)
        self.browse2 = tk.Button(self.f2, bg='orange', command=self.browse_digests)
        
        self.sum = 0
        self.dir = None
        self.file = None
        self.digest = None
    
    def strip_path(self, path):
        words = path.split('/')
        return words[-1]

    def bar(self, blocksz):
        ''' update the progress bar '''
        self.sum += blocksz
        percentage = (self.sum/float(blocksz))
        amt = percentage * self.WIDTH
        #print(amt)
        self.progress['value'] = amt
        self.root.update_idletasks()

    def hash_file(self, isoFile):
        ''' Hash the .iso file with sha256 '''
        #blocksize to read file
        BLOCKSIZE = 4096
        #create hashing obj
        hasher = sha256()
        sz = os.path.getsize(isoFile)
        self.progress = Progressbar(self.root, orient='horizontal', length=self.WIDTH, mode='determinate')
        self.progress.pack()
        with open(isoFile, 'rb') as f:
            print('File length:')
            print(sz)
            while True:
                chunk = f.read(BLOCKSIZE)
                if not chunk:
                    break
                hasher.update(chunk)
                self.bar(sz)
        return hasher.hexdigest()

    def print_out(self, out):
        ''' print output '''
        #self.clickMe.delete(0, len(self.clickMessage))
        if out:
            self.clickMe.configure(text="Match!")
            self.clickMe.configure(background='green')
            self.f3.configure(background='green')
        else:
            self.clickMe.configure(text="No Match!")
            self.clickMe.configure(background='red')

    def auth(self, entry, entry2):
        ''' authenticate file digest against given digest '''
        print(entry)
        print(entry2)        
        #FIXME: check to see if entry2 is a file or a raw digest
        entry = self.strip_path(entry)
        compDigest = self.hash_file(entry)
        digest = get_hashsum(self.strip_path(entry2), entry)
        print('\n')
        print(compDigest)
        print(digest)
        print('sum:')
        print(self.sum)
        self.print_out((compDigest == digest))

    def display(self):
        ''' pack or place components to display them '''
        self.canvas.pack()
        self.header.place(relwidth=1.0, relheight=0.5)
        self.heading.place(relx=0.20, rely=0.21, relwidth=0.7)
        self.heading.insert(tk.END, "SumPy\n", "center")
        self.heading.configure(state='disabled')

        self.frame.place(relx=0.0, rely=0.5, relwidth=1.0, relheight=0.5)
        self.f1.place(relwidth=1.0, relheight=0.33)
        self.f2.place(relx=0.0, rely=0.33, relwidth=1.0, relheight=0.33)
        self.f3.place(relx=0.0, rely=0.66, relwidth=1.0, relheight=0.34)
        
        self.clickMe.place(relwidth=1.0, relheight=1.0)
        self.clickMe.configure(state="disabled")
        self.entry2.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.5)
        self.browse2.place(relx=0.85, rely=0.25, relwidth=0.1, relheight=0.5)

        self.entry.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.5)
        self.browse.place(relx=0.85, rely=0.25, relwidth=0.1, relheight=0.5)

    def run(self):
        ''' run main loop '''
        self.root.mainloop()
        
    def browse_files(self):
        ''' browse files for selection '''
        #FIXME: Change so that file paths also work for OSX/WINDOWS
        self.dir = os.getcwd()
        entry = self.entry.get()
        self.file = filedialog.askopenfilename(initialdir=self.dir, title='Select File')
        self.entry.delete(0, len(entry))
        self.entry.insert(0, self.file)
    
    def browse_digests(self):
        ''' browse digests for selection'''
        self.dir = os.getcwd()
        entry = self.entry2.get()
        self.digest = filedialog.askopenfilename(initialdir=self.dir, title='Select Digest')
        self.entry2.delete(0, len(entry))
        self.entry2.insert(0, self.digest)

def main():
    ''' Start running the application '''
    # create instance of a UI
    ui = UserInterface()
    
    # place all components
    ui.display()
    
    # run app loop
    ui.run()


if __name__ == "__main__":
    main()
