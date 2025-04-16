# 🖼️ Vibixel

**Vibixel** is a Python desktop application that transforms ordinary images into stunning cartoon-style artwork using OpenCV and Tkinter. With adjustable parameters and real-time previews, it’s both a fun tool and a great demonstration of computer vision techniques like edge detection, color quantization, and image smoothing.

---

## 🚀 Features

- 🎨 **Cartoonify Any Image**  
  Transform JPG, PNG, or BMP images into cartoon-style artwork using OpenCV.

- 🧠 **Edge Detection**  
  Adjustable edge intensity to fine-tune the outlines in your cartoon image.

- 🌈 **Color Reduction**  
  Reduce the number of colors using K-means clustering for that flat, comic-book feel.

- 💧 **Smoothing Control**  
  Apply median blur to soften colors and enhance the cartoon effect.

- ⚡ **Real-Time Parameter Adjustment**  
  Instantly preview your changes by adjusting sliders for edge intensity, blur level, and color levels.

- 🧵 **Multithreaded Processing**  
  Keeps the interface responsive during image processing.

- 💾 **Save Your Creation**  
  Export your cartoonified image in PNG, JPEG, or BMP format.

- 📏 **Smart Scaling & Scroll Support**  
  Automatically scales the image to fit the display area, with scrollbars for large images.

- 📂 **Simple GUI**  
  User-friendly interface built with Tkinter — no coding required!

---

## 🛠️ How It Works

The cartoonification process includes:

1. Grayscale conversion and median blur to smooth out noise.  
2. Adaptive thresholding for creating clean edge maps.  
3. Color quantization using K-means clustering.  
4. Median blur applied to the quantized image.  
5. Combining edges with the smoothed, quantized image using bitwise masking.

---

## 🖥️ Requirements

- Python 3.x  
- OpenCV (`opencv-python`)  
- NumPy  
- PIL (`Pillow`)  
- Tkinter (usually included with Python)

### Install dependencies:
```
pip install opencv-python numpy pillow

## 📷 How to Use

1. Run the application:

   ```bash
   python cartoonify_app.py
```
2. Select an image from your computer.
3. Adjust the sliders for Edge Intensity, Color Reduction, and Blur Level.
4. Save the final result using the Save button.

.

## 💡 Future Improvements (Ideas)

- Drag & Drop support for faster file selection
- Side-by-side view of original vs. cartoonified image
- Preset styles (e.g. “Comic Bold”, “Soft Sketch”, “Ink Wash”)
- Batch processing for multiple images at once

## 📬 Feedback
If you like this project, consider giving it a ⭐ on GitHub!
Feel free to open issues or submit PRs for improvements!
