# src/core/ports/gemini_gateway.py
from abc import ABC, abstractmethod
from typing import Dict, Optional


class GeminiGateway(ABC):
    @abstractmethod
    def analyze_text(self, text: str, post_title: str) -> Optional[Dict]:
        pass