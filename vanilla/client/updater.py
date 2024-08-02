import requests
import json
import tkinter as tk
from tkinter import messagebox, ttk
import os
import subprocess
import shutil
from tempfile import TemporaryDirectory
import ttkbootstrap as tb
import stat
import winshell

class Updater:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.root = None
        self.progress_bar = None
        self.spinner = None
        self.start_update_button = None
        self.check_button = None
        self.app_path = "app.exe"

    def get_version_from_server(self):
        """Returns the latest version from the server"""
        response = requests.get(f'{self.base_url}/checklatest')
        response.raise_for_status()
        return response.json()['version']

    def get_current_version(self):
        """Returns the current version from the local version file"""
        version_file = 'version.json'
        if os.path.isfile(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                return json.load(f)['version']
        else:
            return "0"

    def check_for_updates(self):
        """Checks for updates and updates the UI accordingly"""
        self.spinner.pack(pady=10)
        self.spinner.start()
        try:
            server_version = self.get_version_from_server()
            current_version = self.get_current_version()

            if server_version > current_version:
                self.start_update_button.pack(pady=20)
                self.check_button.pack_forget()
            else:
                messagebox.showinfo("No Update", "You have the latest version.")
        except requests.RequestException as e:
            print(e)
            messagebox.showerror("Error", f"Failed to check for updates: {e}")
        finally:
            self.spinner.stop()
            self.spinner.pack_forget()

    def download_update_file(self):
        """Downloads the update file"""
        try:
            url = f'{self.base_url}/update'
            temp_dir = TemporaryDirectory()
            temp_path = os.path.join(temp_dir.name, self.app_path)

            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 8192

            self.progress_bar['value'] = 0
            self.progress_bar['maximum'] = total_size

            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        self.progress_bar['value'] += len(chunk)
                        self.root.update_idletasks()
            return temp_path
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to download update: {e}")
            return None

    def install_update(self, temp_path):
        """Installs the update"""
        try:
            # Ensure the temporary file is executable
            os.chmod(temp_path, os.stat(temp_path).st_mode | stat.S_IEXEC)

            shutil.copy(temp_path, self.app_path)
            os.chmod(self.app_path, os.stat(self.app_path).st_mode | stat.S_IEXEC)
            subprocess.Popen([self.app_path])
            os._exit(0)
        except Exception as e:
            print("Error", f"Failed to open update: {e}")
    
    
    # def download_update_file(self):
    #         """Downloads the update file"""
    #         try:
    #             url = f'{self.base_url}/update'
    #             temp_dir = TemporaryDirectory()
    #             temp_path = os.path.join(temp_dir.name, 'update.zip')

    #             response = requests.get(url, stream=True)
    #             response.raise_for_status()
    #             total_size = int(response.headers.get('content-length', 0))
    #             chunk_size = 8192

    #             self.progress_bar['value'] = 0
    #             self.progress_bar['maximum'] = total_size

    #             with open(temp_path, 'wb') as f:
    #                 for chunk in response.iter_content(chunk_size=chunk_size):
    #                     if chunk:
    #                         f.write(chunk)
    #                         self.progress_bar['value'] += len(chunk)
    #                         self.root.update_idletasks()
    #             return temp_path
    #         except requests.RequestException as e:
    #             messagebox.showerror("Error", f"Failed to download update: {e}")
    #             return None

    # def install_update(self, temp_path):
    #     """Installs the update"""
    #     try:
    #         # Extract the zip file
    #         with zipfile.ZipFile(temp_path, 'r') as zip_file:
    #             zip_file.extractall()

    #         # Copy the updated files
    #         for file in os.listdir('update'):
    #             shutil.copy(os.path.join('update', file), self.app_path)

    #         # Ensure the updated executable is executable
    #         os.chmod(self.app_path, os.stat(self.app_path).st_mode | stat.S_IEXEC)

    #         # Create a shortcut
    #         self.create_shortcut()

    #         # Open the updated executable
    #         subprocess.Popen([self.app_path])
    #         os._exit(0)
    #     except Exception as e:
    #         print("Error", f"Failed to open update: {e}")
    

    def create_shortcut(self):
        """Creates a shortcut on the desktop"""
        try:
            shortcut_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', f'{self.app_path}.lnk')
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
            winshell.shortcut(shortcut_path)
            print(shortcut_path)
            if os.path.exists(shortcut_path):
                print("Shortcut created successfully")
            else:
                print("Failed to create shortcut")
        except Exception as e:
            print("Error creating shortcut:", e)

    def download_update(self):
        """Downloads and installs the update"""
        temp_path = self.download_update_file()
        if temp_path:
            self.create_shortcut()
            self.install_update(temp_path)
            temp_dir = os.path.dirname(temp_path)
            os.rmdir(temp_dir)

    def create_ui(self):
        """Creates the UI for the updater"""
        self.root = tb.Window(themename="flatly")
        self.root.title("Updater")

        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.check_button = ttk.Button(
            frame, text="Check for Updates", command=self.check_for_updates)
        self.check_button.pack(pady=20)

        self.spinner = ttk.Progressbar(frame, mode='indeterminate')
        self.spinner.pack(pady=10)
        self.spinner.pack_forget()

        self.start_update_button = ttk.Button(
            frame, text="Start Update", command=self.download_update)
        self.start_update_button.pack(pady=20)
        self.start_update_button.pack_forget()

        self.progress_bar = ttk.Progressbar(
            frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=20)

    def main(self):
        """Main function that runs the updater"""
        self.create_ui()
        self.root.mainloop()

if __name__ == "__main__":
    updater = Updater()
    updater.main()