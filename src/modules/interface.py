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
        self.root.geometry("12x80+100+100")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)

        self.rodando = False 

        self.set_theme()

        self.container = ctk.CTkFrame(master=root, fg_color=self.bg_color)
        self.container.pack(expand=True, fill="both", padx=5, pady=0)
        self.container.bind("<Button-1>", self.recolher)

        # Criação dos widgets
        
        self.label = ctk.CTkLabel(self.container, text="AutoCodeAtive", font=("Roboto", 12), text_color=self.fg_color)

        self.btn_frame = ctk.CTkFrame(self.container, fg_color=self.bg_color, corner_radius=8)

        self.timer_label = ctk.CTkLabel(self.btn_frame, text="00:00", font=("Roboto", 24, "bold"), text_color=self.fg_color)
        
        self.btn_toggle = self.create_button(self.btn_frame, "▶", self.toggle_automacao)
        self.btn_encerrar = self.create_button(self.btn_frame, "✖", self.encerrar)
        self.tempo_execucao = 0  # segundos
        self.timer_job = None    # controle do after

        self.timer_label.grid(row=0, column=0, padx=(5, 15))
        self.btn_toggle.grid(row=0, column=1, padx=10)
        self.btn_encerrar.grid(row=0, column=2, padx=10)


        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        self.root.bind("<Button-3>", self.toggle_theme)
        self.root.bind("<Enter>", self.expandir)

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
        for btn in [self.btn_toggle, self.btn_encerrar]:
            btn.configure(fg_color=self.bg_color, text_color=self.fg_color, hover_color=self.hover_color)

    def create_button(self, parent, text, command):
        return ctk.CTkButton(parent, text=text, command=command, font=("Roboto", 14, "bold"), width=40,
                             fg_color=self.bg_color, text_color=self.fg_color,
                             hover_color=self.hover_color)
        
    def atualizar_cronometro(self):
        minutos = self.tempo_execucao // 60
        segundos = self.tempo_execucao % 60
        self.timer_label.configure(text=f"{minutos:02}:{segundos:02}")
        self.tempo_execucao += 1
        self.timer_job = self.root.after(1000, self.atualizar_cronometro)

    def toggle_automacao(self):
        if self.rodando:
            pausar_automacao()
            self.btn_toggle.configure(text="▶", text_color=self.fg_color, bg_color=self.bg_color, fg_color=self.bg_color)
            if self.timer_job:
                self.root.after_cancel(self.timer_job)  
        else:
            iniciar_automacao()
            self.btn_toggle.configure(text="🔴", fg_color="#ff4d4d")
            self.atualizar_cronometro()
        self.rodando = not self.rodando

    def encerrar(self):
        encerrar_automacao()
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.tempo_execucao = 0
            self.timer_label.configure(text="00:00")
        self.root.quit()

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self._x
        y = self.root.winfo_pointery() - self._y
        self.root.geometry(f"+{x}+{y}")

    def expandir(self, event):
        self.root.geometry("600x80")
        self.root.attributes("-alpha", 1.0)
        self.label.pack(pady=(8, 0))
        self.btn_frame.pack(pady=(5, 10))        

    def recolher(self, event):
        self.root.geometry("12x80")
        self.root.attributes("-alpha", 0.5)
        self.label.pack_forget()
        self.timer_label.pack_forget()
        self.btn_frame.pack_forget()

if __name__ == "__main__":
    logger.info("Interface iniciada.")
    root = ctk.CTk()
    app = AutomacaoGUI(root)
    root.mainloop()
