import os
from typing import List, Dict, Any, Optional
import json
import requests
from datetime import datetime
import time

from recursive_thinking_base import BaseRecursiveThinkingAgent

class DeepSeekRecursiveThinkingAgent(BaseRecursiveThinkingAgent):
    """DeepSeek implementation of the recursive thinking agent."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "deepseek-chat",
        use_openrouter: bool = False,
        openrouter_model: str = "deepseek/deepseek-chat"
    ):
        """Initialize the DeepSeek agent.

        Args:
            api_key: DeepSeek API key or OpenRouter API key
            model: DeepSeek model to use (for native API)
            use_openrouter: Whether to use OpenRouter instead of native API
            openrouter_model: Model identifier for OpenRouter
        """
        super().__init__(api_key, use_openrouter)

        # Set up API key and model
        if use_openrouter:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            self.model = openrouter_model
        else:
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
            self.model = model
            # Configure DeepSeek API
            self.deepseek_base_url = "https://api.deepseek.com/v1/chat/completions"
            self.deepseek_headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

    def _call_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to DeepSeek or OpenRouter."""
        if self.use_openrouter:
            return self._call_openrouter_api(messages, temperature, stream)
        else:
            return self._call_native_api(messages, temperature, stream)

    def _call_native_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make a native API call to DeepSeek."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            "max_tokens": 4096  # Increase token limit for DeepSeek
        }

        try:
            response = requests.post(
                self.deepseek_base_url,
                headers=self.deepseek_headers,
                json=payload,
                stream=stream
            )
            response.raise_for_status()

            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith("data: "):
                            line = line[6:]
                            if line.strip() == "[DONE]":
                                break
                            try:
                                chunk = json.loads(line)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        full_response += content
                                        print(content, end="", flush=True)
                            except json.JSONDecodeError:
                                continue
                print()  # New line after streaming
                return full_response
            else:
                return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            return "Error: Could not get response from DeepSeek API"

    def _call_openrouter_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to OpenRouter."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            "reasoning": {
                "max_tokens": 10386,
            }
        }

        try:
            response = requests.post(
                self.openrouter_base_url,
                headers=self.openrouter_headers,
                json=payload,
                stream=stream
            )
            response.raise_for_status()

            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith("data: "):
                            line = line[6:]
                            if line.strip() == "[DONE]":
                                break
                            try:
                                chunk = json.loads(line)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        full_response += content
                                        print(content, end="", flush=True)
                            except json.JSONDecodeError:
                                continue
                print()  # New line after streaming
                return full_response
            else:
                return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            return "Error: Could not get response from OpenRouter API"
