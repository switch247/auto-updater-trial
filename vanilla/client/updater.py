import requests
import json
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys
import time
def check_for_updates():
    try:
        response = requests.get('http://localhost:5000/checklatest')
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
                download_update()
        else:
            messagebox.showinfo("No Update", "You have the latest version.")
    except requests.RequestException as e:
        print(e)
        messagebox.showerror("Error", f"Failed to check for updates: {e}")


def download_update():
    try:
        response = requests.get(
            'http://localhost:5000/update/updater.exe', stream=True)
        response.raise_for_status()
        with open('updater.exe', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        # Run the downloaded executable
        if messagebox.askyesno("Update Downloaded", "Update downloaded successfully. Do you want to run the installer?"):
            # Run the downloaded executable in the background
            p = subprocess.Popen(['updater.exe'])
            # Wait for 5 seconds to allow the executable to finish running
            # time.sleep(5)
            # Close the current app
            os._exit(0)
    
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to download update: {e}")


def main():
    root = tk.Tk()
    root.title("Updater test")

    check_button = tk.Button(
        root, text="Check for Updates", command=check_for_updates)
    check_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
