import subprocess
import os
import json
from PyQt5.QtCore import QThread, pyqtSignal

os.environ["QT_QPA_PLATFORM"] = "xcb"

class OllamaWorker(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            # We explicitly tell the AI to prioritize the netlist context
            messages = [
                {
                    "role": "system",
                    "content": ("You are a professional electronic engineer for eSim. "
                                "Use the provided netlist to analyze nodes, components, and connections. "
                                "Explain concisely in at MOST 30 words.")
                },
                {"role": "user", "content": self.user_text}
            ]
            
            # Using JSON dump for robust message passing
            response = subprocess.run(
                ["ollama", "run", "qwen2.5-coder:3b", json.dumps(messages)], 
                capture_output=True, text=True, check=True
            )

            bot_response = response.stdout.strip() or "No response received."
        
        except Exception as e:
            bot_response = f"Error: {str(e)}"

        self.response_signal.emit(bot_response)