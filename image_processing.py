import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1000x800")  # Expanded window size for a better experience
        
        # Initialize variables
        self.image = None  # Original image loaded from file
        self.original_image = None  # Backup of the original image
        self.cropped_image = None  # Cropped image
        self.rect_start = None  # Starting point of the crop rectangle
        self.rect_end = None  # Ending point of the crop rectangle
        self.zoom_factor = 1.0  # Initial zoom factor
        
        # Set maximum canvas dimensions
        self.max_canvas_width = 700
        self.max_canvas_height = 500
        
        # Set up the UI components
        self.create_widgets()

    def create_widgets(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Create a "File" menu in the menu bar
file_menu = tk.Menu(menubar, tearoff=0)  # Create a dropdown menu under "File" with tear-off disabled
menubar.add_cascade(label="File", menu=file_menu)  # Add "File" menu to the menu bar

# Add menu options to the "File" menu
file_menu.add_command(label="Open", command=self.load_image)  # Adds an "Open" option to load an image
file_menu.add_command(label="Save", command=self.save_image)  # Adds a "Save" option to save an image

file_menu.add_separator()  # Adds a separator line for better menu organization

file_menu.add_command(label="Exit", command=self.root.quit)  # Adds an "Exit" option to close the application

        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f7f7f7")
        main_frame.pack(padx=30, pady=30, fill="both", expand=True)
        
        # Canvas Frame (for original and cropped images)
        canvas_frame = tk.Frame(main_frame, bg="#f7f7f7")
        canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Canvas for original image
        self.canvas_original = tk.Canvas(canvas_frame, bg='gray', width=self.max_canvas_width, height=self.max_canvas_height)
        self.canvas_original.grid(row=0, column=0, padx=10)
        
        # Canvas for cropped image
        self.canvas_cropped = tk.Canvas(canvas_frame, bg='white', width=self.max_canvas_width, height=self.max_canvas_height)
        self.canvas_cropped.grid(row=0, column=1, padx=10)

        # Controls Frame
        control_frame = tk.Frame(main_frame, bg="#f7f7f7")
        control_frame.grid(row=1, column=0, pady=20, sticky="ew")
        
        # Crop and Resize Controls
        button_frame = tk.Frame(control_frame, bg="#f7f7f7")
        button_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        
        self.crop_button = tk.Button(button_frame, text="Crop", command=self.activate_crop, width=15, height=2, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", bd=2)
        self.crop_button.grid(row=0, column=0, padx=10)
        
        self.undo_button = tk.Button(button_frame, text="Undo", command=self.undo_crop, width=15, height=2, bg="#FF5722", fg="white", font=("Arial", 12), relief="raised", bd=2)
        self.undo_button.grid(row=0, column=1, padx=10)
        
        self.save_button = tk.Button(button_frame, text="Save", command=self.save_image, width=15, height=2, bg="#2196F3", fg="white", font=("Arial", 12), relief="raised", bd=2)
        self.save_button.grid(row=0, column=2, padx=10)
        
        # Resize Cropped Image Slider
        resize_label = tk.Label(control_frame, text="Resize Cropped Image", font=("Arial", 12))
        resize_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.resize_slider = tk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL, command=self.resize_cropped_image)
        self.resize_slider.set(100)
        self.resize_slider.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief="sunken", anchor="w", font=("Arial", 10))
        self.status_bar.pack(side="bottom", fill="x", padx=5, pady=5)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is not None:
                self.original_image = self.image.copy()
                self.display_image(self.image, self.canvas_original)
                self.status_bar.config(text=f"Loaded: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to load image.")
    
    def save_image(self):
        if self.cropped_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                cv2.imwrite(file_path, self.cropped_image)
                messagebox.showinfo("Image Saved", "Your image has been saved successfully!")
                self.status_bar.config(text=f"Saved: {file_path}")
        else:
            messagebox.showerror("Error", "No image to save!")
root = tk.Tk()
app = ImageEditorApp(root)
root.mainloop()

