import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading

class CartoonifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Cartoonifier")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.original_image = None
        self.cartoon_image = None
        self.processing = False
        self.current_file_path = None
        
        # Create UI elements
        self.create_widgets()
        
        # Start by asking for an image
        self.select_image()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Image display area
        self.image_frame = tk.Frame(self.main_frame, bg='white', bd=2, relief=tk.SUNKEN)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.canvas = tk.Canvas(self.image_frame, bg='white')
        self.scroll_y = ttk.Scrollbar(self.image_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_x = ttk.Scrollbar(self.image_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.control_frame.pack(fill=tk.X)
        
        # Buttons
        self.select_btn = ttk.Button(self.control_frame, text="Select Image", command=self.select_image)
        self.select_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_btn = ttk.Button(self.control_frame, text="Save", command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Parameters controls
        self.params_frame = tk.LabelFrame(self.main_frame, text="Cartoon Parameters", bg='#f0f0f0')
        self.params_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Edge threshold
        tk.Label(self.params_frame, text="Edge Intensity:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.edge_slider = ttk.Scale(self.params_frame, from_=100, to=500, value=300, command=self.update_params)
        self.edge_slider.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Color quantization
        tk.Label(self.params_frame, text="Color Reduction:", bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.color_slider = ttk.Scale(self.params_frame, from_=2, to=20, value=7, command=self.update_params)
        self.color_slider.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Blur level
        tk.Label(self.params_frame, text="Blur Level:", bg='#f0f0f0').grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.blur_slider = ttk.Scale(self.params_frame, from_=1, to=15, value=5, command=self.update_params)
        self.blur_slider.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        self.params_frame.columnconfigure(1, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_image(self):
        if self.processing:
            return
            
        file_path = filedialog.askopenfilename(
            title="Select an Image", 
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        
        if file_path:
            self.current_file_path = file_path
            self.process_image()

    def process_image(self):
        if self.current_file_path is None:
            return
            
        self.processing = True
        self.status_var.set("Processing... Please wait")
        self.save_btn.config(state=tk.DISABLED)
        self.root.update()
        
        # Process in a separate thread to keep UI responsive
        threading.Thread(target=self._process_image_thread, daemon=True).start()

    def _process_image_thread(self):
        try:
            # Read and convert image
            img = cv2.imread(self.current_file_path)
            if img is None:
                raise ValueError("Could not read image file")
                
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(imgRGB)
            
            # Get current parameter values
            edge_thresh = int(self.edge_slider.get())
            color_levels = int(self.color_slider.get())
            blur_level = int(self.blur_slider.get())
            
            # Edge detection
            gray = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2GRAY)
            gray_blur = cv2.medianBlur(gray, blur_level)
            edges = cv2.adaptiveThreshold(gray_blur, 255, 
                                        cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY, 
                                        9, 5)
            
            # Color quantization
            img_quant = self.color_quantization(imgRGB, color_levels)
            
            # Smoothing
            blurred = cv2.medianBlur(img_quant, blur_level)
            
            # Combine edges with quantized image
            cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
            
            # Convert to PIL format
            self.cartoon_image = Image.fromarray(cartoon)
            
            # Update display
            self.root.after(0, self.update_display)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Error processing image"))
        finally:
            self.processing = False
            self.root.after(0, lambda: self.status_var.set("Ready"))

    def color_quantization(self, img, k):
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result

    def update_display(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Display cartoon image
        img = self.cartoon_image.copy()
        
        # Resize to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width() - 20
        canvas_height = self.canvas.winfo_height() - 20
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
            
        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)
            
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to ImageTk format
        imgtk = ImageTk.PhotoImage(img)
        
        # Add image to canvas
        self.canvas.create_image(
            (canvas_width - new_width) // 2, 
            (canvas_height - new_height) // 2, 
            anchor=tk.NW, 
            image=imgtk
        )
        
        # Configure scroll region
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        
        # Keep reference to avoid garbage collection
        self.canvas.imgtk = imgtk
        
        # Enable save button
        self.save_btn.config(state=tk.NORMAL)
        self.status_var.set("Processing complete")

    def update_params(self, event=None):
        if self.current_file_path is not None and not self.processing:
            # Re-process image with new parameters
            self.process_image()

    def save_image(self):
        if self.cartoon_image is None:
            return
            
        output_path = filedialog.asksaveasfilename(
            title="Save Cartoon Image",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg;*.jpeg"),
                ("BMP Image", "*.bmp")
            ]
        )
        
        if output_path:
            try:
                # Convert PIL image to RGB if needed
                if self.cartoon_image.mode != 'RGB':
                    self.cartoon_image = self.cartoon_image.convert('RGB')
                
                self.cartoon_image.save(output_path)
                messagebox.showinfo("Success", f"Image saved successfully to:\n{output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CartoonifyApp(root)
    root.mainloop()