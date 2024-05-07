import speech_recognition as sr
from tkinter import *
from tkinter import filedialog
import googletrans
import textblob
from tkinter import ttk, messagebox
import pyttsx3
import cv2                             #camera recoginition
import pytesseract                     #camera recoginition
from PIL import Image, ImageTk         #camera recoginition
from tkinter import font
from tkinter import PhotoImage
from PIL import Image, ImageTk
from textblob import TextBlob



pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\HP\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'  # Update the path accordingly

def on_entry_click(event):
    if original_text.get("1.0", "end-1c") == "Enter your text..":
        original_text.delete("1.0", END)
        original_text.config(fg="black")

def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Text-to-Speech", e)

def on_translate_click():
    original_content = original_text.get("1.0", "end-1c").strip()

    if original_content == "Enter your text..":
        messagebox.showinfo("Translator", "Please enter text, use voice, or load an image before translating.")
        return

    translated_text.delete("1.0", END)

    try:
        for key, value in languages.items():
            if value == original_combo.get():
                from_language_key = key

        for key, value in languages.items():
            if value == translated_combo.get():
                to_language_key = key

        words = textblob.TextBlob(original_content)

        translated_words = words.translate(from_lang=from_language_key, to=to_language_key)

        translated_text.insert("1.0", translated_words)

    except Exception as e:
        messagebox.showerror("Translator", e)

def play_sound():
    speak_text(translated_text.get("1.0", "end-1c").strip())

def play_sound_original():
    original_content = original_text.get("1.0", "end-1c").strip()
    speak_text(original_content)


def clear():
    original_text.delete("1.0", END)
    original_text.insert("1.0", "Enter your text..")
    original_text.config(fg="#2c3e50")

    translated_text.delete("1.0", END)
    translated_text.insert("1.0", "Your Translated Text, Voice")

def recognize_text_from_camera():
    try:
        # Use OpenCV to capture an image from the camera
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)      #accessing to your webcam to capture the input images
        while True:
             ret, frame = cap.read()                       #reading your webcam and save it in 2 variables
             # Display the captured image
             cv2.imshow("Captured Image", frame)  # create a new window that contains the webcam stream
             if cv2.waitKey(1) & 0xFF == ord('s'):
                 cv2.imwrite("captured_image.png", frame)
                 break

        cap.release()
        cv2.destroyAllWindows()

        # Open the captured image
        img = cv2.imread("captured_image.png")
        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Resize the image to fit the window
        small_width = 200
        small_height = int((small_width / img_rgb.shape[1]) * img_rgb.shape[0])
        img_rgb = cv2.resize(img_rgb, (small_width, small_height))
        # Convert to PIL ImageTk format
        img_tk = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        # Display the image in the Tkinter window
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # Use Tesseract OCR to recognize text from the image
        recognized_text = pytesseract.image_to_string(img)
        # Display the recognized text in the original text box
        original_text.delete("1.0", END)
        original_text.insert("1.0", recognized_text)
        original_text.config(fg="black")

    except Exception as e:
        messagebox.showerror("Image Recognition", e)

def recognize_voice():
    rec = sr.Recognizer()
    with sr.Microphone() as src:
        audio = rec.listen(src)
        recognized_text = rec.recognize_google(audio, language="en")  # Adjust the language if needed
        original_text.delete("1.0", END)
        original_text.insert("1.0", recognized_text)
        original_text.config(fg="black")

def recognize_text_from_image():
    try:
        # Open a file dialog to choose an image
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        # Use OpenCV to read the image
        img = cv2.imread(file_path)

        # Convert the image to RGB (OpenCV uses BGR by default)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize the image to a smaller size
        small_width = 200  # Adjust the width as needed
        small_height = int((small_width / img_rgb.shape[1]) * img_rgb.shape[0])
        img_rgb = cv2.resize(img_rgb, (small_width, small_height))

        # Convert to PIL ImageTk format
        img_tk = ImageTk.PhotoImage(Image.fromarray(img_rgb))

        # Display the image in the bottom left of the screen
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # Use Tesseract OCR to recognize text from the image
        recognized_text = pytesseract.image_to_string(img)

        original_text.delete("1.0", END)
        original_text.insert("1.0", recognized_text)
        original_text.config(fg="black")

    except Exception as e:
        messagebox.showerror("Image Recognition", e)


def toggle_dark_mode():
    current_bg_color = root.cget("bg")
    current_fg_color = root.option_get("Button", "background")

    # Toggle between dark and light modes
    if current_bg_color == "#34495e":  # If currently in dark mode
        root.configure(bg="#EEDFCC")
        root.option_add("*Font", "Helvetica 12")
        toggle_button.config(text="🌙", bg="#34495e", fg="white")
    else:  # If currently in light mode
        root.configure(bg="#34495e")
        root.option_add("*Font", "Helvetica 12")
        toggle_button.config(text="☀", bg="white", fg="#ADFF2F")


def switch_languages():
    original_language = original_combo.get()
    translated_language = translated_combo.get()

    original_combo.set(translated_language)
    translated_combo.set(original_language)

def open_developer_window():
    developer_window = Toplevel(root)
    developer_window.title("ABOUT US")
    developer_window.geometry("400x300")
    developer_label = Label(
        developer_window,
        text="This Project Developed By :\n\n1.Hossam Eltahan",
        font=("Helvetica", 14),
        anchor="w",
        justify="left"
    )
    developer_label.pack(pady=20)


languages = googletrans.LANGUAGES
language_list = list(languages.values())

root = Tk()

img=PhotoImage(file='C:\\Users\\HP\\Translator\\translator.png')
root.iconphoto(False,img)

# Calculate screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate window width and height
window_width = 1200
window_height = 650

# Calculate x and y coordinates for the Tkinter window to be centered
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.maxsize(1400,700)
root.title("FCIT TRANSLATOR")



root.configure(bg="#34495e")
root.option_add("*Font", "Helvetica 12")

for i in range(5):  # Assuming you have 5 rows
    root.grid_rowconfigure(i, weight=1)

for i in range(3):  # Assuming you have 3 columns
    root.grid_columnconfigure(i, weight=1)


style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#3498db", foreground="#ecf0f1")
style.map("TButton", foreground=[("active", "#ecf0f1"), ("pressed", "#ecf0f1")])


original_text = Text(root, height=10, width=50, bg="#ecf0f1", fg="#2c3e50")
original_text.grid(row=0, column=0, pady=20, padx=40)

original_text.insert("1.0", "Enter your text..")
original_text.config(fg="#2c3e50")
original_text.bind("<FocusIn>", on_entry_click)

translate_button = Button(root, text="  Translate  ", font=("Helvetica", 20, "bold"), command=on_translate_click, bg="#007FFF", fg="#000000")
translate_button.grid(row=0, column=1, padx=30,pady=70)

translate_voice_button = Button(root, text="Record🗣🎙", font=("Helvetica", 14, "bold"), command=recognize_voice, bg="#7AC5CD", fg="#000000")
translate_voice_button.grid(row=2, column=2)

translate_image_button = Button(root, text="Device Images🖼", font=("Helvetica", 14, "bold"), command=recognize_text_from_image, bg="#7AC5CD", fg="#000000")
translate_image_button.grid(row=2, column=0, padx=10)


recognize_camera_button = Button(root, text="Take a picture 📸", font=("Helvetica", 14, "bold"), command=recognize_text_from_camera, bg="#7AC5CD", fg="#000000")
recognize_camera_button.grid(row=4, column=0, padx=10)



translated_text = Text(root, height=10, width=50, bg="#ecf0f1", fg="#2c3e50")
translated_text.grid(row=0, column=2, pady=20, padx=0)
translated_text.insert("1.0", "Your Translated Text, Voice")

original_combo = ttk.Combobox(root, width=40, value=language_list, font=("Helvetica", 12), background="#ecf0f1", foreground="#2c3e50")
original_combo.current(21)
original_combo.grid(row=1, column=0,padx=60)

translated_combo = ttk.Combobox(root, width=40, value=language_list, font=("Helvetica", 12), background="#ecf0f1", foreground="#2c3e50")
translated_combo.current(26)
translated_combo.grid(row=1, column=2)

clear_button = Button(root, text="Clear♻", command=clear, font=("Helvetica", 14, "bold"), bg="#e74c3c", fg="#ecf0f1")
clear_button.grid(row=2, column=1, padx=10)


play_sound_button = Button(root, text="🔊", command=play_sound, font=("Helvetica", 14, "bold"), bg="#34495e", fg="#ecf0f1")
play_sound_button.grid(row=1, column=3,sticky="e")

play_sound_button_original = Button(root, text="🔊", command=play_sound_original, font=("Helvetica", 14, "bold"), bg="#34495e", fg="#ecf0f1")
play_sound_button_original.grid(row=1, column=0,sticky="w")


developer_button = Button(root, text="ABOUT US", command=open_developer_window, font=("Helvetica", 12, "bold"), bg="#00688B", fg="#000000")
developer_button.grid(row=4, column=2)

toggle_button = Button(root, text="☀", command=toggle_dark_mode, font=("Helvetica", 16, "bold"), bg="white", fg="#ADFF2F")
toggle_button.grid(row=5, column=3, pady=0,sticky="es")

switch_languages_button = Button(root, text="🔄", command=switch_languages, font=("Helvetica", 14, "bold"), bg="#7AC5CD", fg="#000000")
switch_languages_button.grid(row=1, column=1,pady=0)  


image_label = Label(root, bg="#34495e")
image_label.grid(row=3, column=0, columnspan=10, pady=20)
#hossam
#hossam
root.mainloop()