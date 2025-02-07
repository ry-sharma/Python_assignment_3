import os
import cv2
import tkinter as tk
from tkinter import messagebox

def save_image(folder_path, photo):
    folder_path = "C:/Users/Public/Pictures"  # Hardcoded save location
    if not os.path.exists(folder_path):  # Create folder if it does not exist
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "output.png")
    cv2.imwrite(file_path, photo)  # Save using OpenCV
    messagebox.showinfo("Success", f"Image saved successfully to:\n{file_path}")
    print(f"Image saved to {file_path}")

def get_tk_image(photo):
    coloured_image = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    return tk.PhotoImage(data=cv2.imencode('.ppm', coloured_image)[1].tobytes())

# Example UI window for testing
def create_ui():
    root = tk.Tk()
    root.title("Image Processing App")
    root.geometry("400x200")
    
    tk.Label(root, text="Enhanced Image Saver", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(root, text="Save Image", command=lambda: save_image(None), font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
