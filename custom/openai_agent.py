import os
from typing import List, Dict, Any, Optional
import json
import requests
from datetime import datetime
import time
import openai

from recursive_thinking_base import BaseRecursiveThinkingAgent

class OpenAIRecursiveThinkingAgent(BaseRecursiveThinkingAgent):
    """OpenAI implementation of the recursive thinking agent."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o",
        use_openrouter: bool = False,
        openrouter_model: str = "openai/gpt-4o"
    ):
        """Initialize the OpenAI agent.

        Args:
            api_key: OpenAI API key or OpenRouter API key
            model: OpenAI model to use (for native API)
            use_openrouter: Whether to use OpenRouter instead of native API
            openrouter_model: Model identifier for OpenRouter
        """
        super().__init__(api_key, use_openrouter)

        # Set up API key and model
        if use_openrouter:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            self.model = openrouter_model
        else:
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.model = model
            # Configure OpenAI client
            openai.api_key = self.api_key

    def _call_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to OpenAI or OpenRouter."""
        if self.use_openrouter:
            return self._call_openrouter_api(messages, temperature, stream)
        else:
            return self._call_native_api(messages, temperature, stream)

    def _call_native_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make a native API call to OpenAI."""
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=stream,
                max_tokens=4096  # Increase token limit for OpenAI
            )

            if stream:
                full_response = ""
                for chunk in response:
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            print(content, end="", flush=True)
                print()  # New line after streaming
                return full_response
            else:
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return "Error: Could not get response from OpenAI API"

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
