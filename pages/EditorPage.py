import tkinter as tk
from tkinter import messagebox as mb
from helper.Globalstore import global_store
from helper.DrawSquare import DrawSquareApp
from helper.cvutils import *
import cv2
import numpy as np
from PIL import Image, ImageTk

class EDITORPAGE(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.blur_strength = 0
        self.blured_image = None
        self.real_image = None
        self.slidervalue = None

        # Configure layout
        self.columnconfigure(0, weight=1)  # Sidebar (20%)
        self.columnconfigure(1, weight=4)  # Main editor (80%)
        self.rowconfigure(0, weight=1)

        # Create frames
        menu_frame = tk.Frame(self, bg="#2C3E50", padx=10, pady=10)  # Sidebar with dark theme
        editor_frame = tk.Frame(self, bg="#ECF0F1")  # Light theme for editor
        self.crop_canvas = tk.Canvas(editor_frame, bg="#ECF0F1")

        menu_frame.grid(row=0, column=0, sticky="nsew")
        editor_frame.grid(row=0, column=1, sticky="nsew")

        # File path label
        file_path_label = tk.Label(editor_frame, text=global_store.data['imgPath'], bg="#ECF0F1", fg="#2C3E50", font=("Arial", 10, "bold"))
        file_path_label.pack(fill="x", padx=10, pady=5)

        # Image display
        self.image_edit_label = tk.Label(editor_frame, bg="#BDC3C7", relief="ridge")
        self.image_edit_label.pack(fill="both", expand=True, padx=10, pady=5)
        editor_frame.bind("<Configure>", lambda e: self.resize_image(e, editor_frame, global_store.data['imgPath'], self.image_edit_label))

        # Sidebar buttons
        button_style = {"font": ("Arial", 12, "bold"), "fg": "white", "bg": "#34495E", "bd": 0, "padx": 10, "pady": 5}
        tk.Button(menu_frame, text="New", command=self.show_file_page, **button_style).pack(fill="x", pady=5)
        tk.Button(menu_frame, text="Crop", command=self.crop_image, **button_style).pack(fill="x", pady=5)
        tk.Button(menu_frame, text="Undo", command=self.undo_action, **button_style).pack(fill="x", pady=5)
        tk.Button(menu_frame, text="Save", command=self.save_action, **button_style).pack(fill="x", pady=5)
        
        # Blur slider
        self.blur_slider = tk.Scale(menu_frame, from_=0, to=30, orient="horizontal", label="Blur Image (%)", command=self.blur_image, bg="#2C3E50", fg="white")
        self.blur_slider.set(0)
        self.blur_slider.pack(fill="x", pady=5)

        # Shortcut guide
        suggestion_text = """Shortcut:
        New: Ctrl + N
        Cut: Ctrl + C
        Undo: Ctrl + Z
        Save: Ctrl + S"""
        suggestion = tk.Text(menu_frame, wrap="word", width=30, height=6, bg="#34495E", fg="white", font=("Arial", 10))
        suggestion.insert("1.0", suggestion_text)
        suggestion.config(state="disabled")
        suggestion.pack(fill="x", pady=10)

        # Bind shortcuts
        self.bind_all("<Control-n>", lambda event: self.show_file_page())
        self.bind_all("<Control-c>", lambda event: self.crop_image())
        self.bind_all("<Control-z>", lambda event: self.undo_action())
        self.bind_all("<Control-s>", lambda event: self.save_action())

    def resize_image(self, event, frame, image_path, label):
        new_width, new_height = frame.winfo_width(), frame.winfo_height()
        img = cv2.imread(image_path)
        self.reimg = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        self.real_image = self.reimg
        resized_img_rgb = cv2.cvtColor(self.reimg, cv2.COLOR_BGR2RGB)
        self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', resized_img_rgb)[1].tobytes())
        label.config(image=self.photo)
        label.image = self.photo

    def crop_image(self):
        self.crop_canvas = tk.Canvas(self.image_edit_label, width=self.image_edit_label.winfo_width(), height=self.image_edit_label.winfo_height(), highlightthickness=0)
        self.image_on_canvas = self.crop_canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.crop_canvas.place(x=0, y=0)
        DrawSquareApp(self.crop_canvas, self.reimg)

    def show_file_page(self):
        if mb.askyesno("Confirmation", "Do you want to continue?"):
            self.controller.show_file_upload_page()

    def blur_image(self, scale_value):
        blur_strength = int(scale_value) * 2 + 1
        if self.crop_canvas.winfo_exists():
            self.crop_canvas.place_forget()
        if blur_strength > self.blur_strength:
            self.blur_strength = blur_strength
            blur_image = cv2.GaussianBlur(self.reimg, (blur_strength, blur_strength), 0)
            self.reimg = blur_image
            self.blured_image = blur_image
            coloured_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2RGB)
            self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())
            self.image_edit_label.config(image=self.photo)
            self.image_edit_label.image = self.photo

    def save_action(self):
        if self.crop_canvas.winfo_exists():
            self.crop_canvas.place_forget()
        save_image("output", self.blured_image if self.is_cv2_image(self.blured_image) else self.reimg)

    def undo_action(self):
        if self.crop_canvas.winfo_exists():
            self.crop_canvas.place_forget()
        self.blur_slider.set(0)
        self.blur_strength = 0
        self.reimg = self.real_image
        coloured_image = cv2.cvtColor(self.real_image, cv2.COLOR_BGR2RGB)
        self.photo = tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())
        self.image_edit_label.config(image=self.photo)
        self.image_edit_label.image = self.photo
        self.blured_image = None

    def is_cv2_image(self, var):
        return isinstance(var, np.ndarray)
