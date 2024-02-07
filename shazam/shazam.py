import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import asyncio
from shazamio import Shazam
import threading


def print_keys_values(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key) + ": ", end='')
        if isinstance(value, dict):
            print()
            print_keys_values(value, indent + 1)
        elif isinstance(value, list):
            print()
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    print('\t' * (indent + 1) + f"Item {i+1}:")
                    print_keys_values(item, indent + 2)
                else:
                    print('\t' * (indent + 1) + str(item))
        else:
            print(str(value))

# 將異步操作適配為可以在新線程中運行的函數
def recognize_song_async(filename, callback):
    async def async_recognize_song():
        shazam = Shazam()
        out = await shazam.recognize_song(filename)
        return out['track']['title']

    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(async_recognize_song())
        loop.close()
        callback(result)  # 處理结果的回調函數

    threading.Thread(target=run).start()

# 更新 GUI 的回調函數
def update_gui_with_result(result):
    result_text = str(result)
    text_area.configure(state='normal')
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, result_text)
    text_area.configure(state='disabled')

# 彈出文件選擇對話框並處理選中的文件
def select_file_and_recognize():
    filename = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.ogg *.m4a"), ("All Files", "*.*"))
    )
    if filename:
        recognize_song_async(filename, update_gui_with_result)

# 創建 GUI
root = tk.Tk()
root.title("Shazam Song Recognizer")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 添加按鈕
select_file_btn = ttk.Button(frame, text="Select Song and Recognize", command=select_file_and_recognize)
select_file_btn.grid(row=0, column=0, pady=10, padx=5, sticky=(tk.W, tk.E))

# 添加滾動文本框以顯示结果
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15, state='disabled')
text_area.grid(row=1, column=0, pady=10, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
