import os
import sys
import logging
import tkinter as tk
from modules.interface import AutomacaoGUI

# Define pasta segura para o log
log_dir = os.path.join(os.environ.get('LOCALAPPDATA', '.'), 'AutoCodeAtive')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'automacao.log')

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("Interface iniciada.")
    root = tk.Tk()
    app = AutomacaoGUI(root)
    root.mainloop()
