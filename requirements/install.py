import subprocess
import sys

def install_dependencies():
    subprocess.call([sys.executable, "-m", "pip", "install", "-r", "dev.txt"])

if __name__ == "__main__":
    install_dependencies()