import os
from typing import List, Dict, Any, Optional, Tuple
import json
import requests
from datetime import datetime
import time

class BaseRecursiveThinkingAgent:
    """Base class for recursive thinking agents with common functionality."""

    def __init__(self, api_key: str = None, use_openrouter: bool = False):
        """Initialize the base agent.

        Args:
            api_key: API key for the service
            use_openrouter: Whether to use OpenRouter instead of native API
        """
        self.api_key = api_key
        self.use_openrouter = use_openrouter
        self.conversation_history = []
        self.full_thinking_log = []

        # OpenRouter configuration
        self.openrouter_base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.openrouter_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Recursive Thinking Chat",
            "Content-Type": "application/json"
        }

    def _call_api(self, messages: List[Dict], temperature: float = 0.7, stream: bool = True) -> str:
        """Make an API call to the LLM service.

        This method should be implemented by subclasses.

        Args:
            messages: List of message dictionaries with role and content
            temperature: Temperature for response generation
            stream: Whether to stream the response

        Returns:
            The generated response as a string
        """
        raise NotImplementedError("Subclasses must implement _call_api")

    def _determine_thinking_rounds(self, prompt: str) -> int:
        """Let the model decide how many rounds of thinking are needed."""
        meta_prompt = f"""Given this message: "{prompt}"

How many rounds of iterative thinking (1-5) would be optimal to generate the best response?
Consider the complexity and nuance required.
Respond with just a number between 1 and 5."""

        messages = [{"role": "user", "content": meta_prompt}]

        print("\n=== DETERMINING THINKING ROUNDS ===")
        response = self._call_api(messages, temperature=0.3, stream=True)
        print("=" * 50 + "\n")

        try:
            rounds = int(''.join(filter(str.isdigit, response)))
            return min(max(rounds, 1), 5)
        except:
            return 3

    def _generate_alternatives(self, base_response: str, prompt: str, num_alternatives: int = 3) -> List[str]:
        """Generate alternative responses.

        Args:
            base_response: The current best response
            prompt: The original user prompt
            num_alternatives: Number of alternative responses to generate

        Returns:
            A list of alternative responses
        """
        alternatives = []

        for i in range(num_alternatives):
            print(f"\n=== GENERATING ALTERNATIVE {i+1}/{num_alternatives} ===")
            alt_prompt = f"""Original message: {prompt}

Current response: {base_response}

Generate an alternative response that might be better. Be creative and consider different approaches.
Alternative response:"""

            messages = self.conversation_history + [{"role": "user", "content": alt_prompt}]
            alternative = self._call_api(messages, temperature=0.7 + i * 0.1, stream=True)
            alternatives.append(alternative)
            print("=" * 50)

        return alternatives

    def _evaluate_responses(self, prompt: str, current_best: str, alternatives: List[str]) -> Tuple[str, str]:
        """Evaluate responses and select the best one."""
        print("\n=== EVALUATING RESPONSES ===")
        eval_prompt = f"""Original message: {prompt}

Evaluate these responses and choose the best one:

Current best: {current_best}

Alternatives:
{chr(10).join([f"{i+1}. {alt}" for i, alt in enumerate(alternatives)])}

Which response best addresses the original message? Consider accuracy, clarity, and completeness.
First, respond with ONLY 'current' or a number (1-{len(alternatives)}).
Then on a new line, explain your choice in one sentence."""

        messages = [{"role": "user", "content": eval_prompt}]
        evaluation = self._call_api(messages, temperature=0.2, stream=True)
        print("=" * 50)

        # Better parsing
        lines = [line.strip() for line in evaluation.split('\n') if line.strip()]

        choice = 'current'
        explanation = "No explanation provided"

        if lines:
            first_line = lines[0].lower()
            if 'current' in first_line:
                choice = 'current'
            else:
                for char in first_line:
                    if char.isdigit():
                        choice = char
                        break

            if len(lines) > 1:
                explanation = ' '.join(lines[1:])

        if choice == 'current':
            return current_best, explanation
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(alternatives):
                    return alternatives[index], explanation
            except:
                pass

        return current_best, explanation

    def think_and_respond(self, user_input: str, verbose: bool = True, num_alternatives: int = 3) -> Dict:
        """Process user input with recursive thinking.

        Args:
            user_input: The user's input
            verbose: Whether to print verbose output
            num_alternatives: Number of alternative responses to generate in each round

        Returns:
            A dictionary containing the response, thinking rounds, and thinking history
        """
        print("\n" + "=" * 50)
        print("🤔 RECURSIVE THINKING PROCESS STARTING")
        print("=" * 50)

        thinking_rounds = self._determine_thinking_rounds(user_input)

        if verbose:
            print(f"\n🤔 Thinking... ({thinking_rounds} rounds needed)")

        # Initial response
        print("\n=== GENERATING INITIAL RESPONSE ===")
        messages = self.conversation_history + [{"role": "user", "content": user_input}]
        current_best = self._call_api(messages, stream=True)
        print("=" * 50)

        thinking_history = [{"round": 0, "response": current_best, "selected": True}]

        # Iterative improvement
        for round_num in range(1, thinking_rounds + 1):
            if verbose:
                print(f"\n=== ROUND {round_num}/{thinking_rounds} ===")

            # Generate alternatives
            alternatives = self._generate_alternatives(current_best, user_input, num_alternatives)

            # Store alternatives in history
            for i, alt in enumerate(alternatives):
                thinking_history.append({
                    "round": round_num,
                    "response": alt,
                    "selected": False,
                    "alternative_number": i + 1
                })

            # Evaluate and select best
            new_best, explanation = self._evaluate_responses(user_input, current_best, alternatives)

            # Update selection in history
            if new_best != current_best:
                for item in thinking_history:
                    if item["round"] == round_num and item["response"] == new_best:
                        item["selected"] = True
                        item["explanation"] = explanation
                current_best = new_best

                if verbose:
                    print(f"\n    ✓ Selected alternative: {explanation}")
            else:
                for item in thinking_history:
                    if item["selected"] and item["response"] == current_best:
                        item["explanation"] = explanation
                        break

                if verbose:
                    print(f"\n    ✓ Kept current response: {explanation}")

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": current_best})

        # Keep conversation history manageable
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        # Add to full thinking log
        self.full_thinking_log.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "final_response": current_best,
            "thinking_rounds": thinking_rounds,
            "thinking_history": thinking_history
        })

        print("\n" + "=" * 50)
        print("🎯 FINAL RESPONSE SELECTED")
        print("=" * 50)

        result = {
            "response": current_best,
            "thinking_rounds": thinking_rounds,
            "thinking_history": thinking_history
        }

        return result

    def save_full_log(self, filename: str = None):
        """Save the full thinking process log."""
        if filename is None:
            filename = f"full_thinking_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "conversation": self.conversation_history,
                "full_thinking_log": self.full_thinking_log,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)

        print(f"Full thinking log saved to {filename}")

    def save_conversation(self, filename: str = None):
        """Save the conversation and thinking history."""
        if filename is None:
            filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "conversation": self.conversation_history,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)

        print(f"Conversation saved to {filename}")

    def save_response_as_markdown(self, user_input: str, result: Dict, folder: str = "responses"):
        """Save the response in markdown format.

        Args:
            user_input: The user's input
            result: The result dictionary from think_and_respond
            folder: The folder to save the response in
        """
        # Create the folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Create a truncated version of the user input for the filename
        # Remove special characters and limit to 30 characters
        safe_input = ''.join(c if c.isalnum() or c.isspace() else '_' for c in user_input)
        truncated_input = safe_input[:30].strip().replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{folder}/{truncated_input}_{timestamp}.md"

        # Create the markdown content
        markdown = f"""# Response to: {user_input}

## Final Response
{result['response']}

## Thinking Process

**Number of thinking rounds:** {result['thinking_rounds']}

"""

        # Add the thinking history
        for item in result['thinking_history']:
            selection_status = "✅ SELECTED" if item['selected'] else "❌ ALTERNATIVE"
            markdown += f"### Round {item['round']} - {selection_status}\n\n"
            markdown += f"{item['response']}\n\n"
            if 'explanation' in item and item['selected']:
                markdown += f"**Reason for selection:** {item['explanation']}\n\n"
            markdown += "---\n\n"

        # Save the markdown file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"Response saved as markdown to {filename}")
