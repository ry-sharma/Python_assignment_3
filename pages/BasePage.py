import tkinter as tk
from .FileUploadPage import FILEUPLOADPAGE
from .EditorPage import EDITORPAGE

class APP(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)

        # Window configurations
        self.title("Image Processing App")
        self.geometry("1200x800")
        self.configure(bg="#2C3E50")  # Dark background color
        self.wm_state('zoomed')

        # Creating a styled container
        self.container = tk.Frame(self, bg="#ECF0F1", padx=10, pady=10)  
        self.container.pack(fill="both", expand=True)

        # Initializing frames
        self.current_frame = None
        self.show_file_upload_page()  # Show file upload page first
       
    def show_file_upload_page(self):    
        """Function to activate the file upload page"""    
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = FILEUPLOADPAGE(self.container, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
    def show_editor_page(self):
        """Function to activate the editor page"""        
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = EDITORPAGE(self.container, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

        
        
  
   
        
  
