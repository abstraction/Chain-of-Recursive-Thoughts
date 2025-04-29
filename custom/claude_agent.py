import os
from typing import List, Dict, Any, Optional
import json
import requests
from datetime import datetime
import time
import anthropic

from recursive_thinking_base import BaseRecursiveThinkingAgent

class ClaudeRecursiveThinkingAgent(BaseRecursiveThinkingAgent):
    """Claude implementation of the recursive thinking agent."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "claude-3-opus-20240229",
        use_openrouter: bool = False,
        openrouter_model: str = "anthropic/claude-3-opus-20240229"
    ):
        """Initialize the Claude agent.

        Args:
            api_key: Anthropic API key or OpenRouter API key
            model: Claude model to use (for native API)
            use_openrouter: Whether to use OpenRouter instead of native API
            openrouter_model: Model identifier for OpenRouter
        """
        super().__init__(api_key, use_openrouter)

        # Set up API key and model
        if use_openrouter:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            self.model = openrouter_model
        else:
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            self.model = model
            # Configure Anthropic client
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def _call_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to Claude or OpenRouter."""
        if self.use_openrouter:
            return self._call_openrouter_api(messages, temperature, stream)
        else:
            return self._call_native_api(messages, temperature, stream)

    def _call_native_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make a native API call to Anthropic's Claude."""
        try:
            # Convert messages to Claude format
            claude_messages = self._convert_to_claude_messages(messages)

            response = self.client.messages.create(
                model=self.model,
                messages=claude_messages,
                temperature=temperature,
                stream=stream,
                max_tokens=8192  # Increased token limit for Claude
            )

            if stream:
                full_response = ""
                for chunk in response:
                    if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                        content = chunk.delta.text
                        if content:
                            full_response += content
                            print(content, end="", flush=True)
                print()  # New line after streaming
                return full_response
            else:
                return response.content[0].text
        except Exception as e:
            print(f"Claude API Error: {e}")
            return "Error: Could not get response from Claude API"

    def _convert_to_claude_messages(self, messages: List[Dict]) -> List[Dict]:
        """Convert standard chat messages to Claude's format."""
        claude_messages = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                # System messages are handled differently in Claude
                # We'll prepend them to the first user message
                continue
            elif role == "user":
                claude_messages.append({"role": "user", "content": content})
            elif role == "assistant":
                claude_messages.append({"role": "assistant", "content": content})

        return claude_messages

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
