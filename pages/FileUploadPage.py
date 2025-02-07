import tkinter as tk
from widgets.FileUpload import FILEUPLOAD
from tkinter import filedialog
from widgets.ErrorMssage import ErrorMessage
from .EditorPage import EDITORPAGE
from helper.Globalstore import global_store


class FILEUPLOADPAGE(tk.Frame):
    upload_controller = None

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.upload_controller = controller
        self.configure(bg="#f0f0f0")  # Light gray background

        # Canvas for file display
        self.file_canvas = tk.Canvas(self, width=500, height=200, bg="white", highlightthickness=2, highlightbackground="#ccc")
        self.file_canvas.pack(pady=20)

        # Upload button
        self.upload_button = tk.Button(
            self, text="Upload Image", font=("Arial", 12, "bold"),
            bg="#007BFF", fg="white", padx=10, pady=5, cursor="hand2",
            command=self.upload_action
        )
        self.upload_button.pack(pady=10)

        # Label to show selected file
        self.file_label = tk.Label(self, text="No file selected", font=("Arial", 10), fg="gray", bg="#f0f0f0")
        self.file_label.pack()

        # Initialize FileUpload widget
        f = FILEUPLOAD(self.file_canvas, upload_action=self.upload_action)
        self.image_path = f.get_image_path()

        # Bind Ctrl+O shortcut for file selection
        self.bind_all("<Control-o>", lambda event: self.upload_action())

    def upload_action(self):
        """Function to open the file selector"""
        filename = filedialog.askopenfilename(title="Select an Image",
                                              filetypes=[("Image Files", "*.jpg *.png *.jpeg")])

        file_error_msg = ErrorMessage(self.file_canvas, "Please choose a valid image file!")  

        if filename.endswith(('.jpg', '.png', '.jpeg')):
            self.file = filename
            global_store.data["imgPath"] = filename  # Store file path globally

            # Update file label with selected file name
            self.file_label.config(text=f"Selected: {filename.split('/')[-1]}", fg="green")

            # Hide error message and proceed to editor page
            file_error_msg.hide()
            self.upload_controller.show_editor_page()
        else:
            self.file_label.config(text="Invalid file! Please select a valid image.", fg="red")
            file_error_msg.show(250, 150, "center")
