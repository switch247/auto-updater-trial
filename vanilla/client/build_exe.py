import subprocess

def run_pyinstaller():
    subprocess.run(["pyinstaller", "--onefile", "updater.py"])

if __name__ == "__main__":
    run_pyinstaller()