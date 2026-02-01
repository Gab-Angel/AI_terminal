import time
import sys
from threading import Thread, Event


class MatrixSpinner:
    """Spinner animado estilo Matrix"""
    
    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def __init__(self, text: str = "Processando"):
        self.text = text
        self.stop_event = Event()
        self.thread = None
    
    def _animate(self):
        idx = 0
        while not self.stop_event.is_set():
            frame = self.FRAMES[idx % len(self.FRAMES)]
            sys.stdout.write(f'\r\033[92m{frame}\033[0m \033[36m{self.text}...\033[0m')
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
    
    def start(self):
        self.stop_event.clear()
        self.thread = Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=0.5)


class TypingEffect:
    """Efeito de digitação"""
    
    @staticmethod
    def print(text: str, speed: float = 0.015, color: str = '\033[92m'):
        for char in text:
            sys.stdout.write(color + char + '\033[0m')
            sys.stdout.flush()
            time.sleep(speed)
        print()