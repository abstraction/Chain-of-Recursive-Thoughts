import os
from typing import List, Dict, Any, Optional
import json
import requests
from datetime import datetime
import time

from recursive_thinking_base import BaseRecursiveThinkingAgent

class LocalLMStudioAgent(BaseRecursiveThinkingAgent):
    """Local LLM implementation using LM Studio API for the recursive thinking agent."""

    def __init__(
        self,
        api_url: str = "http://localhost:1234/v1",
        model: str = None,
        use_openrouter: bool = False,
        openrouter_api_key: str = None,
        openrouter_model: str = "openai/gpt-3.5-turbo"
    ):
        """Initialize the Local LM Studio agent.

        Args:
            api_url: URL for the LM Studio API (default: http://localhost:1234/v1)
            model: Model name (optional for LM Studio as it's configured in the UI)
            use_openrouter: Whether to use OpenRouter instead of local API
            openrouter_api_key: API key for OpenRouter (if use_openrouter is True)
            openrouter_model: Model identifier for OpenRouter
        """
        # If using OpenRouter, we need an API key
        if use_openrouter:
            api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OpenRouter API key is required when use_openrouter is True")
        else:
            api_key = None  # Local LM Studio doesn't need an API key

        super().__init__(api_key, use_openrouter)

        # Set up API URL and model
        if use_openrouter:
            self.model = openrouter_model
        else:
            self.api_url = api_url
            self.model = model  # Can be None for LM Studio as it's configured in the UI
            self.headers = {
                "Content-Type": "application/json"
            }

    def _call_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to LM Studio or OpenRouter."""
        if self.use_openrouter:
            return self._call_openrouter_api(messages, temperature, stream)
        else:
            return self._call_local_api(messages, temperature, stream)

    def _call_local_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make a local API call to LM Studio."""
        endpoint = f"{self.api_url}/chat/completions"

        payload = {
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            "max_tokens": 4096  # Increase token limit for local models
        }

        # Add model if specified (optional for LM Studio)
        if self.model:
            payload["model"] = self.model

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
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
            print(f"LM Studio API Error: {e}")
            return "Error: Could not get response from LM Studio API"

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
