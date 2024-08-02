import tkinter as tk
from tkinter import messagebox
import subprocess
from ttkbootstrap import Style
import requests
import json
import os

def check_for_updates():
    try:
        BaseUrl =  "http://localhost:5000"
        response = requests.get(f'{BaseUrl}/checklatest')
        response.raise_for_status()
        server_version = response.json()['version']
        version_file = 'version.json'
        updates_directory = "./"
        files = os.listdir(updates_directory)
        file_list = [f for f in files if os.path.isfile(os.path.join(updates_directory, f))]
        print(file_list)
        current_version = "0"
        if os.path.isfile('./version.json'):
            with open(version_file, 'r', encoding='utf-8') as f:
                current_version = json.load(f)['version']
        else:
            print("file not found")
        if server_version > current_version:
            if messagebox.askyesno("Update Available", "A new version is available. Do you want to update?"):
                open_updater()
        else:
            messagebox.showinfo("No Update", "You have the latest version.")
    except requests.RequestException as e:
        print(e)
        messagebox.showerror("Error", f"Failed to check for updates: {e}")

def open_updater():
    subprocess.Popen(['updater.exe'])
    os._exit(0)

def main():
    root = tk.Tk()
    style = Style('cosmo')
    root.title("Main Application")
    root.geometry("300x200")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    button = tk.ttk.Button(frame, text="Check for Updates", command=check_for_updates, style="TButton")
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
