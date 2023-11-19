# -*- coding: utf-8 -*-
import os
from tkinter import *
from PIL import Image, ImageTk
import subprocess

path = '/'

if os.name == 'nt':
    os.chdir("C:\\")
else:
    os.chdir(path)

class Finder():
    def __init__(self, root):
        self.root = root
        self.root.title("Finder")
        self.root.geometry("800x400")

        self.photo_images = []
        self.image_objects = []
        self.thumbnail_size = (100, 100)

        # 添加滚动条
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=BOTH, expand=True)
        self.canvas_scrollbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        self.canvas_scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas = Canvas(self.canvas_frame, bg="white", yscrollcommand=self.canvas_scrollbar.set)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas_scrollbar.config(command=self.canvas.yview)

        self.load_icons()

        self.display_files_and_folders()

        self.canvas.bind("<Configure>", self.on_canvas_configure)  # 绑定Canvas大小调整事件
        self.root.bind("<Command-Z>", self.return_folder)
        self.root.bind("<Control-Z>", self.return_folder)
        self.root.bind("<Option-Up>", self.return_folder)   # macOS Option+Up
        self.root.bind("<Alt-Up>", self.return_folder)      # Windows Option+Up

    def load_icons(self):
        self.folder_icon = self.get_image("Folder.png", 100, 100)
        self.file_icon = self.get_image("File.png", 100, 100)
        self.display_files_and_folders()

    def get_image(self, filename, width, height):
        image_path = os.path.join(os.path.dirname(__file__), filename)
        im = Image.open(image_path).resize((width, height))
        return ImageTk.PhotoImage(im)

    def display_files_and_folders(self):
        current_path = path
        x_offset = 10
        y_offset = 20
        max_width = self.root.winfo_width() - 150
        item_count = 0
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isfile(item_path):
                file_image = self.canvas.create_image(x_offset, y_offset, image=self.file_icon, anchor='nw')
                file_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                self.make_draggable(file_image, file_text)
                self.canvas.tag_bind(file_image, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                self.canvas.tag_bind(file_text, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                item_count += 1
                if item_count == 5:
                    item_count = 0
                    x_offset = 10
                    y_offset += 150
                else:
                    x_offset += 150
            elif os.path.isdir(item_path):
                folder_image = self.canvas.create_image(x_offset, y_offset, image=self.folder_icon, anchor='nw')
                folder_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                self.make_draggable(folder_image, folder_text)
                self.canvas.tag_bind(folder_image, '<Double-Button-1>', lambda event, path=item_path: self.display_folder_contents(path))
                self.canvas.tag_bind(folder_text, '<Double-Button-1>', lambda event, path=item_path: self.display_folder_contents(path))
                item_count += 1
                if item_count == 5:
                    item_count = 0
                    x_offset = 10
                    y_offset += 150
                else:
                    x_offset += 150

            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def return_folder(self, event):
        current_path = os.getcwd()
        parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
        os.chdir(parent_path)  # 更改当前工作目录到上一级目录
        self.display_folder_contents(parent_path)  # 显示上一级目录的内容

    def open_file(self, file_path):
        if os.name == 'nt':
            os.startfile(file_path)
        else:
            subprocess.call(['open', file_path])

    def display_folder_contents(self, folder_path):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.delete("all")
        x_offset = 10
        y_offset = 20
        max_width = self.root.winfo_width() - 150
        item_count = 0
        os.chdir(folder_path)
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                file_image = self.canvas.create_image(x_offset, y_offset, image=self.file_icon, anchor='nw')
                file_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                self.make_draggable(file_image, file_text)
                self.canvas.tag_bind(file_image, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                self.canvas.tag_bind(file_text, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                item_count += 1
                if item_count == 5:
                    item_count = 0
                    x_offset = 10
                    y_offset += 150
                else:
                    x_offset += 150
            elif os.path.isdir(item_path):
                folder_image = self.canvas.create_image(x_offset, y_offset, image=self.folder_icon, anchor='nw')
                folder_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                self.make_draggable(folder_image, folder_text)
                self.canvas.tag_bind(folder_image, '<Double-Button-1>', lambda event, path=item_path: self.display_folder_contents(path))
                self.canvas.tag_bind(folder_text, '<Double-Button-1>', lambda event, path=item_path: self.display_folder_contents(path))
                item_count += 1
                if item_count == 5:
                    item_count = 0
                    x_offset = 10
                    y_offset += 150
                else:
                    x_offset += 150

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<Configure>", self.on_canvas_configure)  # 重新绑定Canvas大小调整事件
        self.root.bind("<Command-z>", self.return_folder)  # 重新绑定键盘绑定
        self.root.bind("<Control-z>", self.return_folder)  # 重新绑定键盘绑定

    def on_canvas_configure(self, event):  # Canvas大小调整事件处理方法
        self.canvas.itemconfig(self.canvas_frame, width=event.width, height=event.height)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def make_draggable(self, image_id, text_id):
        self.canvas.tag_bind(image_id, '<ButtonPress-1>', lambda event: self.on_drag_start(event, image_id, text_id))
        self.canvas.tag_bind(image_id, '<B1-Motion>', lambda event: self.on_drag_motion(event, image_id, text_id))
        self.canvas.tag_bind(text_id, '<ButtonPress-1>', lambda event: self.on_drag_start(event, image_id, text_id))
        self.canvas.tag_bind(text_id, '<B1-Motion>', lambda event: self.on_drag_motion(event, image_id, text_id))

    def on_drag_start(self, event, image_id, text_id):
        self._drag_data = {'image_id': image_id, 'text_id': text_id, 'x': event.x, 'y': event.y}

    def on_drag_motion(self, event, image_id, text_id):
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        self.canvas.move(image_id, delta_x, delta_y)
        self.canvas.move(text_id, delta_x, delta_y)
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

root = Tk()
finder = Finder(root)
root.mainloop()
