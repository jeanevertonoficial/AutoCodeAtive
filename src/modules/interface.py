import customtkinter as ctk
import logging
from modules.automacao import iniciar_automacao, pausar_automacao, encerrar_automacao

logger = logging.getLogger(__name__)
modo_escuro = True

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AutomacaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry("15x80+100+100")
        self.root.attributes("-topmost", True)

        self.set_theme()

        self.container = ctk.CTkFrame(master=root, corner_radius=12, fg_color=self.bg_color)
        self.container.pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(self.container, text="AutoCodeAtive", font=("Roboto", 10), text_color=self.fg_color)
        self.label.pack(pady=(8, 0))

        self.btn_frame = ctk.CTkFrame(self.container, fg_color=self.bg_color, corner_radius=8)
        self.btn_frame.pack(pady=(5, 10))

        self.btn_iniciar = self.create_button(self.btn_frame, "▶", self.iniciar)
        self.btn_pausar = self.create_button(self.btn_frame, "⏸", self.pausar)
        self.btn_encerrar = self.create_button(self.btn_frame, "✖", self.encerrar)

        self.btn_iniciar.grid(row=0, column=0, padx=10)
        self.btn_pausar.grid(row=0, column=1, padx=10)
        self.btn_encerrar.grid(row=0, column=2, padx=10)

        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.root.bind("<Button-3>", self.toggle_theme)

    def set_theme(self):
        global modo_escuro
        if modo_escuro:
            self.bg_color = "#1e1e1e"
            self.fg_color = "#e6e6e6"
            self.hover_color = "#2a2a2a"
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#002b36"
            self.hover_color = "#e0e0e0"
        self.root.configure(bg=self.bg_color)

    def toggle_theme(self, event=None):
        global modo_escuro
        modo_escuro = not modo_escuro
        self.set_theme()
        self.container.configure(fg_color=self.bg_color)
        self.label.configure(text_color=self.fg_color)
        self.btn_frame.configure(fg_color=self.bg_color)
        for btn in [self.btn_iniciar, self.btn_pausar, self.btn_encerrar]:
            btn.configure(fg_color=self.bg_color, text_color=self.fg_color, hover_color=self.hover_color)

    def create_button(self, parent, text, command):
        return ctk.CTkButton(parent, text=text, command=command, font=("Roboto", 12), width=40,
                             fg_color=self.bg_color, text_color=self.fg_color,
                             hover_color=self.hover_color, corner_radius=8)

    def iniciar(self):
            iniciar_automacao()

    def pausar(self):
        pausar_automacao()

    def encerrar(self):
        encerrar_automacao()
        self.root.quit()

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self._x
        y = self.root.winfo_pointery() - self._y
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    logger.info("Interface iniciada.")
    root = ctk.CTk()
    app = AutomacaoGUI(root)
    root.mainloop()
