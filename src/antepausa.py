import logging
import tkinter as tk
from modules.interface import AutomacaoGUI

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automacao.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("Interface iniciada.")
    root = tk.Tk()
    app = AutomacaoGUI(root)
    root.mainloop()
