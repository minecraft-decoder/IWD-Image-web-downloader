import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

# --- ВМІСТ ОРИГІНАЛЬНИХ ФАЙЛІВ ---

APP_PYW_CONTENT = '''import os
import re
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_LDLL_PATH = os.path.join(BASE_DIR, "bin", "web.LDLL")

def log_message(message):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, f"> {message}\\n")
    console_text.see(tk.END)
    console_text.config(state=tk.DISABLED)

def extract_urls_from_file(filepath):
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    raw_lines = [line.strip() for line in content.splitlines() if line.strip()]
    urls = []
    
    for item in raw_lines:
        if "install" in item.lower():
            continue
        
        if not (item.startswith("http://") or item.startswith("https://")):
            item = "https://" + item
            
        urls.append(item)
        
    return urls

def download_single_image(url, index):
    try:
        filename = f"downloaded_image_{index}.png"
        filepath = os.path.join(BASE_DIR, filename)
        log_message(f"Завантаження {index}: {url}")
        
        urllib.request.urlretrieve(url, filepath)
        log_message(f"УСПІХ: Картинка {index} встановлена! ({filename})")
        return True
    except Exception as e:
        log_message(f"ПОМИЛКА завантаження {index}: {e}")
        return False

def download_all_images(urls):
    log_message("--- Початок завантаження всех URL ---")
    success_count = 0
    for idx, url in enumerate(urls, start=1):
        if download_single_image(url, idx):
            success_count += 1
            
    log_message(f"--- Завершено: успішно {success_count} з {len(urls)} ---")
    if success_count > 0:
        messagebox.showinfo("Успіх", f"Успішно встановлено картинок: {success_count}")
    else:
        messagebox.showerror("Помилка", "Не вдалося завантажити жодної картинки.")

root = tk.Tk()
root.title("App Viewer")
root.geometry("550x420")

buttons_frame = tk.Frame(root)
buttons_frame.pack(fill=tk.X, padx=10, pady=10)

urls_list = extract_urls_from_file(WEB_LDLL_PATH)

if not urls_list:
    lbl_empty = ttk.Label(buttons_frame, text="Коректних URL у bin/web.LDLL не знайдено.")
    lbl_empty.pack(pady=5)
else:
    for idx, url in enumerate(urls_list, start=1):
        btn = ttk.Button(
            buttons_frame, 
            text=f"Завантажити картинку {idx}", 
            command=lambda u=url, i=idx: [download_single_image(u, i), messagebox.showinfo("Успіх", f"Картинка {i} встановлена!")]
        )
        btn.pack(fill=tk.X, pady=2)

    if len(urls_list) > 1:
        btn_all = ttk.Button(
            buttons_frame, 
            text=f"Завантажити всі URL ({len(urls_list)})", 
            command=lambda: download_all_images(urls_list)
        )
        btn_all.pack(fill=tk.X, pady=(8, 2))

console_frame = tk.LabelFrame(root, text="Міні-консоль")
console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

console_text = tk.Text(console_frame, bg="black", fg="lime", font=("Consolas", 10), wrap=tk.WORD)
console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(console_frame, orient=tk.VERTICAL, command=console_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
console_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

log_message("Програму запущено.")
log_message(f"Знайдено URL у bin/web.LDLL: {len(urls_list)}")
for i, u in enumerate(urls_list, 1):
    log_message(f"  [{i}] {u}")

root.mainloop()
'''

URL_FIX_CONTENT = '''import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_LDLL_PATH = os.path.join(BASE_DIR, "bin", "web.LDLL")

def fix_url():
    if not os.path.exists(WEB_LDLL_PATH):
        print(f"Помилка: Файл {WEB_LDLL_PATH} не знайдено!")
        return

    with open(WEB_LDLL_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    print(f"Поточний вміст web.LDLL: '{content}'")

    if "install" in content.lower() or not content:
        new_url = "https://picsum.photos/300/300"
        print(f"Замінюємо некоректний вміст на робоче посилання: {new_url}")
    elif not (content.startswith("http://") or content.startswith("https://")):
        new_url = "https://" + content
        print(f"Додано протокол https://: {new_url}")
    else:
        new_url = content
        print("URL вже коректний, змін не потрібно.")

    with open(WEB_LDLL_PATH, "w", encoding="utf-8") as f:
        f.write(new_url)

    print("Файл bin/web.LDLL успішно оновлено!")

if __name__ == "__main__":
    fix_url()
'''

WINLIB_CONTENT = """kernel*wintef
import {lib^webinf }
{
        start bitool
		      stop kerenef
			  
			                 }"""

LINUXLIB_CONTENT = """kernel*fertine
import {lib^webing for linux}
{
        start bitll
		      stop tererntf 
			  
			                 }"""

MACLIB_CONTENT = """kernel*macfer
import {lib^webing for MacOS}
{
        star regtip
		      stop fertin
			  
			                 }"""

README_CONTENT = 'start a "app.py"'

WEB_LDLL_CONTENT = """https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRnvLKL0c8G4yTf19r5ATectZdJClLq97bCeZ9_aZ2yA&s=10
https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdN3xgYXuUWhAZiBbmy9dxCyjN8uwF7ICSLMnVygFg2Q&s=10"""

# --- ЛОГІКА НАВІГАЦІЇ ПО ЕТАПАХ ---

def go_to_step2():
    """Перехід з Етапу 1 (Вітання) на Етап 2 (Вибір компонентів)"""
    frame_step1.pack_forget()
    frame_step2.pack(expand=True, fill="both")

def go_to_step3():
    """Перехід з Етапу 2 (Вибір) на Етап 3 (Встановлення) після перевірки"""
    if not (var_win.get() or var_linux.get() or var_mac.get()):
        messagebox.showwarning("Увага", "Будь ласка, виберіть щонайменше одну бібліотеку для встановлення!")
        return
    
    frame_step2.pack_forget()
    frame_step3.pack(expand=True, fill="both")
    
    start_installation()

def start_installation():
    base_dir = get_base_dir()
    app_dir = base_dir / "app"
    
    # Обов'язкові файли
    files_to_create = {
        app_dir / "app.pyw": APP_PYW_CONTENT,
        app_dir / "URL_fix.py": URL_FIX_CONTENT,
        app_dir / "readme.txt": README_CONTENT,
        app_dir / "bin" / "web.LDLL": WEB_LDLL_CONTENT,
    }
    
    # Додаємо вибрані бібліотеки
    if var_win.get():
        files_to_create[app_dir / "lib" / "winlib.LLB"] = WINLIB_CONTENT
    if var_linux.get():
        files_to_create[app_dir / "lib" / "linuxlib.LLB"] = LINUXLIB_CONTENT
    if var_mac.get():
        files_to_create[app_dir / "lib" / "Maclib.LLB"] = MACLIB_CONTENT

    web_dir = app_dir / "web"
    total_items = len(files_to_create) + 1
    progress_bar["maximum"] = total_items
    progress_bar["value"] = 0
    
    try:
        current = 0
        
        # Створення порожньої папки web/
        web_dir.mkdir(parents=True, exist_ok=True)
        current += 1
        progress_bar["value"] = current
        status_label.config(text=f"Створення папки: {web_dir.relative_to(base_dir)}")
        root.update_idletasks()
        time.sleep(0.15)
        
        # Запис файлів
        for file_path, content in files_to_create.items():
            current += 1
            status_label.config(text=f"Створення: {file_path.relative_to(base_dir)}")
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            
            time.sleep(0.15)
            progress_bar["value"] = current
            root.update_idletasks()
            
        status_label.config(text="Встановлення успішно завершено!", fg="green")
        messagebox.showinfo("Успіх", f"Встановлення успішно завершено!\nПапку 'app' створено в:\n{app_dir}")
        
    except Exception as e:
        status_label.config(text="Помилка при встановленні", fg="red")
        messagebox.showerror("Помилка", f"Не вдалося виконати встановлення:\n{e}")

# --- ГОЛОВНЕ ВІКНО (853x481) ---

root = tk.Tk()
root.title("інсталятор")
root.geometry("853x481")

# Змінні для збереження стану галочок
var_win = tk.BooleanVar(value=True)
var_linux = tk.BooleanVar(value=True)
var_mac = tk.BooleanVar(value=True)


# ================= ЕТАП 1: КНОПКА ВСТАНОВЛЕННЯ =================
frame_step1 = tk.Frame(root)
frame_step1.pack(expand=True, fill="both")

center_frame1 = tk.Frame(frame_step1)
center_frame1.place(relx=0.5, rely=0.5, anchor="center")

title_step1 = tk.Label(center_frame1, text="Майстер встановлення App Viewer", font=("Arial", 16, "bold"))
title_step1.pack(pady=10)

info_step1 = tk.Label(center_frame1, text="Натисніть кнопку нижче, щоб розпочати налаштування та встановлення", font=("Arial", 11))
info_step1.pack(pady=10)

btn_start_install = tk.Button(
    center_frame1, 
    text="Встановити", 
    command=go_to_step2, 
    font=("Arial", 13, "bold"), 
    padx=25, 
    pady=10
)
btn_start_install.pack(pady=15)


# ================= ЕТАП 2: ВИБІР БІБЛІОТЕК =================
frame_step2 = tk.Frame(root)

center_frame2 = tk.Frame(frame_step2)
center_frame2.place(relx=0.5, rely=0.5, anchor="center")

title_step2 = tk.Label(center_frame2, text="Вибір компонентів для встановлення", font=("Arial", 15, "bold"))
title_step2.pack(pady=(0, 5))

# Маленький підказковий текст
note_label = tk.Label(
    center_frame2, 
    text="* Необхідно вибрати як мінімум 1 бібліотеку", 
    font=("Arial", 9, "italic"), 
    fg="gray"
)
note_label.pack(pady=(0, 15))

# Галочки (Checkbuttons)
chk_frame = tk.Frame(center_frame2)
chk_frame.pack(pady=5)

chk_win = tk.Checkbutton(chk_frame, text="Windows Library (winlib.LLB)", variable=var_win, font=("Arial", 11))
chk_win.pack(anchor="w", pady=3)

chk_linux = tk.Checkbutton(chk_frame, text="Linux Library (linuxlib.LLB)", variable=var_linux, font=("Arial", 11))
chk_linux.pack(anchor="w", pady=3)

chk_mac = tk.Checkbutton(chk_frame, text="MacOS Library (Maclib.LLB)", variable=var_mac, font=("Arial", 11))
chk_mac.pack(anchor="w", pady=3)

btn_next_step3 = tk.Button(
    center_frame2, 
    text="Далі >", 
    command=go_to_step3, 
    font=("Arial", 12, "bold"), 
    padx=25, 
    pady=8
)
btn_next_step3.pack(pady=20)


# ================= ЕТАП 3: ПРОЦЕС ВСТАНОВЛЕННЯ =================
frame_step3 = tk.Frame(root)

center_frame3 = tk.Frame(frame_step3)
center_frame3.place(relx=0.5, rely=0.5, anchor="center")

title_step3 = tk.Label(center_frame3, text="Розпаковка файлів...", font=("Arial", 15, "bold"))
title_step3.pack(pady=10)

info_step3 = tk.Label(center_frame3, text="Будь ласка, зачекайте, поки завантаження та створення файлів завершиться.", font=("Arial", 10))
info_step3.pack(pady=5)

progress_bar = ttk.Progressbar(center_frame3, orient="horizontal", length=450, mode="determinate")
progress_bar.pack(pady=15)

status_label = tk.Label(center_frame3, text="Підготовка...", font=("Arial", 10), fg="gray")
status_label.pack(pady=5)

root.mainloop()