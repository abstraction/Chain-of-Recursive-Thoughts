import os
from typing import List, Dict, Any, Optional
import json
import requests
from datetime import datetime
import time
import google.genai as genai

from recursive_thinking_base import BaseRecursiveThinkingAgent

class GeminiRecursiveThinkingAgent(BaseRecursiveThinkingAgent):
    """Gemini implementation of the recursive thinking agent."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-1.5-pro",
        use_openrouter: bool = False,
        openrouter_model: str = "google/gemini-1.5-pro"
    ):
        """Initialize the Gemini agent.

        Args:
            api_key: Google AI API key or OpenRouter API key
            model: Gemini model to use (for native API)
            use_openrouter: Whether to use OpenRouter instead of native API
            openrouter_model: Model identifier for OpenRouter
        """
        super().__init__(api_key, use_openrouter)

        # Set up API key and model
        if use_openrouter:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            self.model = openrouter_model
        else:
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
            self.model = model
            # Create Gemini client
            self.client = genai.Client(api_key=self.api_key)

    def _call_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to Gemini or OpenRouter."""
        if self.use_openrouter:
            return self._call_openrouter_api(messages, temperature, stream)
        else:
            return self._call_native_api(messages, temperature, stream)

    def _call_native_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make a native API call to Google's Gemini."""
        try:
            # Convert messages to Gemini format
            gemini_messages = self._convert_to_gemini_messages(messages)

            # Generate content using the client
            if stream:
                response = self.client.models.generate_content_stream(
                    model=self.model,
                    contents=gemini_messages,
                    config=genai.types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=8192,
                    )
                )

                full_response = ""
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        content = chunk.text
                        if content:
                            full_response += content
                            print(content, end="", flush=True)
                print()  # New line after streaming
                return full_response
            else:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=gemini_messages,
                    config=genai.types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=8192,
                    )
                )
                return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "Error: Could not get response from Gemini API"

    def _convert_to_gemini_messages(self, messages: List[Dict]) -> List[Dict]:
        """Convert standard chat messages to Gemini's format."""
        gemini_messages = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                # Add system message as user message with special prefix
                gemini_messages.append(genai.types.Content(
                    role="user",
                    parts=[genai.types.Part.from_text(f"System: {content}")]
                ))
            elif role == "user":
                gemini_messages.append(genai.types.Content(
                    role="user",
                    parts=[genai.types.Part.from_text(content)]
                ))
            elif role == "assistant":
                gemini_messages.append(genai.types.Content(
                    role="model",
                    parts=[genai.types.Part.from_text(content)]
                ))

        return gemini_messages

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
