import customtkinter as ctk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import os
import threading
import time

# Глобальные переменные для отслеживания прогресса
processed_files = 0
total_files = 0
start_time = 0
is_running = False
current_language = "English"

# Символы для анимации загрузки
loading_symbols = ["|", "/", "-", "\\"]
current_symbol_index = 0

# Текстовые метки для разных языков
labels = {
    "English": {
        "title": "Convert WAV, FLAC, OGG and M4A to MP3",
        "choose_files": "Choose Files",
        "choose_directory": "Save to",
        "start_button": "Convert",
        "progress_label": "Progress: 0%",
        "time_label": "0 min 0 sec",
        "size_label": "0/0",
        "lang_button": "en"
    },
    "Ukrainian": {
        "title": "Конвертація WAV, FLAC, OGG і M4A в MP3",
        "choose_files": "Вибрати файли",
        "choose_directory": "Зберегти в",
        "start_button": "Конвертувати",
        "progress_label": "Прогрес: 0%",
        "time_label": "0 хв 0 сек",
        "size_label": "0/0",
        "lang_button": "укр"
    }
}

def change_language():
    global current_language
    current_language = "Ukrainian" if current_language == "English" else "English"
    update_labels()

def update_labels():
    root.title(labels[current_language]["title"])
    title_label.configure(text=labels[current_language]["title"])
    start_button.configure(text=labels[current_language]["start_button"])
    percent_label.configure(text=labels[current_language]["progress_label"])
    time_label.configure(text=labels[current_language]["time_label"])
    size_label.configure(text=labels[current_language]["size_label"])
    lang_button.configure(text=labels[current_language]["lang_button"])
    choose_files_button.configure(text=labels[current_language]["choose_files"])
    choose_directory_button.configure(text=labels[current_language]["choose_directory"])

def convert_to_mp3(input_file, output_file):
    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="mp3", parameters=["-aq", "0"], tags=None)
    except Exception as e:
        messagebox.showerror("Error", f"Error converting file: {e}")

def choose_files(entry):
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav *.flac *.ogg *.m4a *.mpeg4")])
    if not files:
        entry.configure(placeholder_text="Please choose files (error)" if current_language == "English" else "Виберіть файли (помилка)")
    else:
        entry.delete(0, ctk.END)
        entry.insert(0, ";".join(files))
        entry.configure(placeholder_text="")

def choose_output_directory(entry):
    directory = filedialog.askdirectory()
    if not directory:
        entry.configure(placeholder_text="Please choose a directory (error)" if current_language == "English" else "Виберіть директорію (помилка)")
    else:
        entry.delete(0, ctk.END)
        entry.insert(0, directory)
        entry.configure(placeholder_text="")

def run_conversion(input_files, output_directory):
    global processed_files, total_files, start_time, is_running

    start_time = time.time()
    total_files = len(input_files)
    processed_files = 0
    is_running = True

    for file in input_files:
        if not is_running:
            break
        output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file))[0]}.mp3")
        convert_to_mp3(file, output_file_path)
        processed_files += 1
        time.sleep(0.05)

    is_running = False

def start_conversion():
    global is_running, current_symbol_index

    input_files = input_entry.get().split(";")
    output_directory = output_entry.get()
    if not input_files[0]:
        input_entry.configure(placeholder_text="Please choose files (error)" if current_language == "English" else "Виберіть файли (помилка)")
        return
    if not output_directory:
        output_entry.configure(placeholder_text="Please choose a directory (error)" if current_language == "English" else "Виберіть директорію (помилка)")
        return

    if is_running:
        messagebox.showwarning("Warning", "Process already running" if current_language == "English" else "Процес уже запущено.")
        return

    progress_bar.set(0)
    percent_label.configure(text="Progress: 0%" if current_language == "English" else "Прогрес: 0%")
    size_label.configure(text="0/0")

    threading.Thread(target=run_conversion, args=(input_files, output_directory)).start()

    def update_progress():
        global current_symbol_index

        elapsed_time = time.time() - start_time
        percent_complete = (processed_files / total_files) * 100 if total_files > 0 else 0
        size_label.configure(text=f"{processed_files}/{total_files}")
        time_label.configure(text=f"{int(elapsed_time // 60)} мин {int(elapsed_time % 60)} сек" if current_language == "English" else f"{int(elapsed_time // 60)} хв {int(elapsed_time % 60)} сек")
        percent_label.configure(text=f"Progress: {percent_complete:.1f}%" if current_language == "English" else f"Прогрес: {percent_complete:.1f}%")
        progress_bar.set(percent_complete / 100)

        loading_label.configure(text=loading_symbols[current_symbol_index])
        current_symbol_index = (current_symbol_index + 1) % len(loading_symbols)

        root.update_idletasks()
        if is_running:
            root.after(100, update_progress)
        else:
            loading_label.configure(text="")
            if percent_complete == 100.0:
                messagebox.showinfo("Complete", "Conversion complete!" if current_language == "English" else "Конвертацію завершено!")

    root.after(100, update_progress)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(labels[current_language]["title"])

title_label = ctk.CTkLabel(root, text=labels[current_language]["title"], font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")

lang_button = ctk.CTkButton(root, text=labels[current_language]["lang_button"], command=change_language, width=40)
lang_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

input_entry = ctk.CTkEntry(root, width=250, placeholder_text="")
input_entry.grid(row=1, column=1, padx=10, pady=10)
choose_files_button = ctk.CTkButton(root, text=labels[current_language]["choose_files"], command=lambda: choose_files(input_entry))
choose_files_button.grid(row=1, column=2, padx=10, pady=10)

output_entry = ctk.CTkEntry(root, width=250, placeholder_text="")
output_entry.grid(row=2, column=1, padx=10, pady=10)
choose_directory_button = ctk.CTkButton(root, text=labels[current_language]["choose_directory"], command=lambda: choose_output_directory(output_entry))
choose_directory_button.grid(row=2, column=2, padx=10, pady=10)

frame = ctk.CTkFrame(root)
frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

percent_label = ctk.CTkLabel(frame, text=labels[current_language]["progress_label"])
percent_label.grid(row=0, column=1, padx=10)

progress_bar = ctk.CTkProgressBar(frame, orientation='horizontal', mode='determinate', width=250)
progress_bar.grid(row=0, column=2, padx=20)
progress_bar.set(0)

time_label = ctk.CTkLabel(frame, text=labels[current_language]["time_label"])
time_label.grid(row=0, column=3, padx=10)

empty_label = ctk.CTkLabel(frame, text="")
empty_label.grid(row=1, column=1, padx=10)

size_label = ctk.CTkLabel(frame, text=labels[current_language]["size_label"])
size_label.grid(row=1, column=2, padx=10)

loading_label = ctk.CTkLabel(frame, text="")
loading_label.grid(row=1, column=3, padx=10)

start_button = ctk.CTkButton(root, text=labels[current_language]["start_button"], command=start_conversion)
start_button.grid(row=4, column=0, columnspan=3, pady=10)

# Запускаем главное окно приложения
root.mainloop()
