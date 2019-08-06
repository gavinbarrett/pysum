import os
import tkinter as tk
from tkinter import filedialog

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
        self.f3 = tk.Button(self.frame, bg='purple', command=lambda: self.auth(self.entry.get(), self.entry2.get()))
        self.clickMe = tk.Text(self.f3, bg='purple', font=('Lucida Console', 25), bd=0, highlightthickness=0)

        
        self.entry = tk.Entry(self.f1, font=('Lucida Console', 35), bg='green')
        self.entry2 = tk.Entry(self.f2, font=('Lucida Console', 35), bg='green')
        self.browse = tk.Button(self.f1, bg='orange', command=self.browse_files)
        self.browse2 = tk.Button(self.f2, bg='orange', command=self.browse_digests)

        
        self.dir = None
        self.file = None
        self.digest = None
    
    def auth(self, entry, entry2):
        ''' authenticate file digest against given digest '''
        print(entry)
        print(entry2)        
        #FIXME: check to see if entry2 is a file or a raw digest

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
        self.clickMe.place(relx=0.32, rely=0.25)
        self.clickMe.insert(tk.END, "click here to hash\n", "center")
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
