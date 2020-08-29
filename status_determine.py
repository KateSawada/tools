import tkinter as tk
from functools import partialmethod
import os
from PIL import Image, ImageTk
import json
import collections as cl





class Application(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("720x720")
        super().__init__()
        self.pack()

        self.files = os.listdir()
        self.files_num = len(self.files)
        self.idx = 0
        self.roundness_lst = []
        self.sharpness_lst = []
        self.size_lst = []

        self.create_widgets()
        self.root.bind('<Right>', self.enter_callback)
        self.root.mainloop()

    def btn_exit_click(self):
        self.write_json()
        exit()

    def create_widgets(self):

        self.roundness_label = tk.Label(text="丸み")
        self.roundness_label.pack()
        self.roundness_entry = tk.Entry()
        self.roundness_entry.pack()
        self.sharpness_label = tk.Label(text="鋭さ")
        self.sharpness_label.pack()
        self.sharpness_entry = tk.Entry()
        self.sharpness_entry.pack()
        self.size_label = tk.Label(text="大きさ")
        self.size_label.pack()
        self.size_entry = tk.Entry()
        self.size_entry.pack()
        self.btn_exit = tk.Button(text="終了", command=self.btn_exit_click)
        self.btn_exit.pack()

        while self.files[self.idx][-3:] != "png":
            self.idx += 1
        self.img = ImageTk.PhotoImage(Image.open(self.files[self.idx]))

        self.canvas = tk.Canvas(bg="black", width=360, height=360)
        self.canvas.pack()
        self.image_on_canvas = self.canvas.create_image(180, 180, image=self.img)
        self.roundness_entry.focus_set()
        
    def enter_callback(self, event):
        #取得
        self.roundness_lst.append(self.roundness_entry.get())
        self.sharpness_lst.append(self.sharpness_entry.get())
        self.size_lst.append(self.size_entry.get())
        #クリア
        self.sharpness_entry.delete(0, tk.END)
        self.roundness_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)
        #フォーカス
        self.roundness_entry.focus_set()

        #JSONに書き込み
        self.idx += 1
        if self.idx >= self.files_num:
            self.write_json()
            exit()
        else:
            while self.files[self.idx][-3:] != "png":
                self.idx += 1
                if self.idx >= self.files_num:
                    self.write_json()
                    exit()
            self.img = ImageTk.PhotoImage(Image.open(self.files[self.idx]))
            self.canvas.itemconfig(self.image_on_canvas, image=self.img)
        
        #input()
    def write_json(self):
        ys = cl.OrderedDict()
        others = 0
        for i in range(len(self.roundness_lst)):
            #print(i + others)
            while self.files[i + others][-3:] != "png":
                others += 1
            ys[self.files[i + others]] = [self.roundness_lst[i], self.sharpness_lst[i], self.size_lst[i]]
        fw = open('stone_status.json','w')
        json.dump(ys,fw,indent=4)
        fw.close()

    
    """
    for file in files:
        idx += 1
        img = ImageTk.PhotoImage(Image.open(files[idx]))
        canvas.itemconfig(image_on_canvas, image=img)
        print(file)
        canvas.pack()
        input("next")
    """
if __name__ == "__main__":

    Application()