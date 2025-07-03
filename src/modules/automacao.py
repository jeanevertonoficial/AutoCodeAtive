import ctypes
import time
import pyautogui
import pygetwindow as gw
import random
import logging
import threading
from plyer import notification

logger = logging.getLogger(__name__)

rodando = False
pausado = False

def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def mostrar_notificacao(titulo, mensagem):
    try:
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=5  # segundos
        )
    except Exception as e:
        logger.warning(f"Erro ao exibir notificação: {e}")

def usuario_interagiu(timeout=1.0, intervalo=0.1):
    pos_inicial = pyautogui.position()
    tempo_passado = 0.0
    while tempo_passado < timeout:
        time.sleep(intervalo)
        if pyautogui.position() != pos_inicial:
            mostrar_notificacao("Automação Cancelada", "Usuário interferiu com o mouse.")
            logger.info("Usuário interferiu com o mouse. Ação automática cancelada.")
            return True
        tempo_passado += intervalo
    return False

def acao_automatica():
    mostrar_notificacao("Automação Iniciada", "Script de automação está rodando.")
    logger.info("Executando ação automática.")
    time.sleep(1)

    if usuario_interagiu():
        return

    pyautogui.moveTo(800, 450, duration=0.5)
    if usuario_interagiu():
        return
    time.sleep(0.5)

    for _ in range(5):
        x = random.randint(0, pyautogui.size().width)
        y = random.randint(0, pyautogui.size().height)
        pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.6))
        if usuario_interagiu():
            return
        if random.random() > 0.5:
            pyautogui.click()
            logger.info(f"Movimento para ({x}, {y}) com clique.")
        else:
            logger.info(f"Movimento para ({x}, {y}) sem clique.")
        time.sleep(random.uniform(0.3, 0.7))

    x = random.randint(0, pyautogui.size().width)
    y = random.randint(0, pyautogui.size().height)
    pyautogui.moveTo(x, y, duration=0.6)
    logger.info(f"Movimento final para ({x}, {y}).")

def loop_automacao():
    global rodando, pausado
    tempo_limite = 15 * 60  # 15 minutos em segundos
    start_time = time.time()

    while rodando:
        if not pausado:
            tempo_inativo = get_idle_duration()
            if tempo_inativo > 60:
                logger.info(f"Usuário inativo por {tempo_inativo:.2f}s. Iniciando ação.")
                acao_automatica()
                time.sleep(60)

        # Verifica se o tempo já passou de 15 minutos
        tempo_passado = time.time() - start_time
        if tempo_passado >= tempo_limite:
            logger.info("Tempo limite de execução atingido. Encerrando automação.")
            mostrar_notificacao("Automação Encerrada", "Tempo limite de 15 minutos atingido.")
            encerrar_automacao()
            break

        time.sleep(5)

def iniciar_automacao():
    global rodando, pausado
    if not rodando:
        rodando = True
        pausado = False
        threading.Thread(target=loop_automacao, daemon=True).start()
        logger.info("Automação iniciada.")

def pausar_automacao():
    global pausado
    pausado = not pausado
    mostrar_notificacao("Automação Pausada" if pausado else "Automação Retomada",
                         "A automação foi pausada." if pausado else "A automação foi retomada.")   
    logger.info("Automação pausada." if pausado else "Automação retomada.")

def encerrar_automacao():
    global rodando
    rodando = False
    mostrar_notificacao("Automação Encerrada", "A automação foi encerrada.")
    logger.info("Encerrando automação.")
