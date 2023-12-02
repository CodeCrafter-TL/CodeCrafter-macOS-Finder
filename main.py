# -*- coding: utf-8 -*-
import os
from tkinter import *
from PIL import Image, ImageTk
import tkintertools as tkt
import subprocess
from pygame import mixer

if os.name == 'nt': path = 'C:\\'
else: path = '/'

if os.name == 'nt':
    os.chdir("C:\\")
else:
    os.chdir(path)

class Finder:
    def __init__(self, root):
        self.root = root
        self.root.title("Finder")
        self.root.geometry("800x400")

        self.photo_images = []
        self.image_objects = []
        self.thumbnail_size = (100, 100)
        self.thumbnail_photos = []

        self.folder_icon = self.get_image("Folder.png", 100, 100)
        self.file_icon = self.get_image("File.png", 100, 100)
        self.music_icon = self.get_image("music.png", 100, 100)

        self.root.resizable(False, False)

        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=BOTH, expand=True)
        self.canvas_scrollbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        self.canvas_scrollbar.pack(side=RIGHT, fill=Y)

        self.lefttool = Frame(self.root, width=200, height=400)
        # self.lefttool.place(x=0, y=0, width=200, height=400)

        self.return_tool = Button(self.lefttool, relief=FLAT, text='<', command=self.return_folder)
        self.return_tool.place(x=0, y=0, width=20, height=20)

        self.canvas = Canvas(self.canvas_frame, bg="white", yscrollcommand=self.canvas_scrollbar.set, height=400, width=600)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas_scrollbar.config(command=self.canvas.yview)

        self.load_icons()

        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def load_icons(self):
        self.folder_icon = self.get_image("Folder.png", 100, 100)
        self.display_files_and_folders()
    
    def play_music(self, music_file):
        mixer.init()
        mixer.music.load(music_file)
        mixer.music.play()

    def get_image(self, filename, width, height):
        image_path = os.path.join(os.path.dirname(__file__), filename)
        im = Image.open(image_path).resize((width, height))
        return ImageTk.PhotoImage(im)

    def display_files_and_folders(self):
        current_path = path
        x_offset = 210
        y_offset = 20
        max_width = self.root.winfo_width() - 150
        item_count = 0
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isfile(item_path):
                if item_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.icns', '.ico')):
                    thumbnail_image = Image.open(item_path).resize(self.thumbnail_size)
                    thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
                    self.thumbnail_photos.append(thumbnail_photo)
                    file_image = self.canvas.create_image(x_offset, y_offset, image=self.thumbnail_photos[-1], anchor='nw')
                    db_click = True
                elif item_path.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):  # 添加对音乐文件的处理
                    file_image = self.canvas.create_image(x_offset, y_offset, image=self.music_icon, anchor='nw')
                    file_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                    self.make_draggable(file_image, file_text)
                    db_click = False
                else:
                    # 使用file_icon
                    file_image = self.canvas.create_image(x_offset, y_offset, image=self.file_icon, anchor='nw')
                    db_click = True
                    file_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                self.make_draggable(file_image, file_text)
                if db_click:
                    self.canvas.tag_bind(file_image, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                    self.canvas.tag_bind(file_text, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                else:
                    self.canvas.tag_bind(file_image, '<Double-Button-1>', lambda event, path=item_path: self.play_music(path))
                    self.canvas.tag_bind(file_text, '<Double-Button-1>', lambda event, path=item_path: self.play_music(path))
                item_count += 1
                if item_count == 4:
                    item_count = 0
                    x_offset = 210
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
                if item_count == 4:
                    item_count = 0
                    x_offset = 210
                    y_offset += 150
                else:
                    x_offset += 150

            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def return_folder(self):
        current_path = os.getcwd()
        parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
        os.chdir(parent_path)
        self.display_folder_contents(parent_path)

    def open_file(self, file_path):
        if os.name == 'nt':
            os.startfile(file_path)
        else:
            subprocess.call(['open', file_path])

    def display_folder_contents(self, folder_path):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.delete("all")
        x_offset = 210
        y_offset = 20
        max_width = self.root.winfo_width() - 150
        item_count = 0
        os.chdir(folder_path)
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                if item_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    thumbnail_image = Image.open(item_path).resize(self.thumbnail_size)
                    thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
                    self.thumbnail_photos.append(thumbnail_photo)
                    file_image = self.canvas.create_image(x_offset, y_offset, image=self.thumbnail_photos[-1], anchor='nw')
                    db_click = True
                elif item_path.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):  # 添加对音乐文件的处理
                    file_image = self.canvas.create_image(x_offset, y_offset, image=self.music_icon, anchor='nw')
                    file_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                    self.make_draggable(file_image, file_text)
                    db_click = False
                else:
                    # 使用file_icon
                    file_image = self.canvas.create_image(x_offset, y_offset, image=self.file_icon, anchor='nw')
                    db_click = True
                file_text = self.canvas.create_text(x_offset + 50, y_offset + 120, text=item, anchor='center', width=100)
                self.make_draggable(file_image, file_text)
                if db_click:
                    self.canvas.tag_bind(file_image, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                    self.canvas.tag_bind(file_text, '<Double-Button-1>', lambda event, path=item_path: self.open_file(path))
                else: # 播放音乐
                    self.canvas.tag_bind(file_image, '<Double-Button-1>', lambda event, path=item_path: self.play_music(path))
                    self.canvas.tag_bind(file_text, '<Double-Button-1>', lambda event, path=item_path: self.play_music(path))
                item_count += 1
                if item_count == 4:
                    item_count = 0
                    x_offset = 210
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
                if item_count == 4:
                    item_count = 0
                    x_offset = 210
                    y_offset += 150
                else:
                    x_offset += 150

            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.config(width=event.width, height=event.height)
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
