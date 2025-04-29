import os
import sys
import importlib
from typing import Dict, Any, Optional
import argparse
from datetime import datetime

# Import the base agent implementation
from recursive_thinking_base import BaseRecursiveThinkingAgent

# We'll use lazy imports for the specific agent implementations

def get_api_key(provider: str, use_openrouter: bool) -> str:
    """Get the API key for the specified provider."""
    # Local LM Studio doesn't need an API key unless using OpenRouter
    if provider == "local" and not use_openrouter:
        return None

    if use_openrouter:
        key_name = "OPENROUTER_API_KEY"
        provider_name = "OpenRouter"
    else:
        if provider == "openai":
            key_name = "OPENAI_API_KEY"
            provider_name = "OpenAI"
        elif provider == "claude":
            key_name = "ANTHROPIC_API_KEY"
            provider_name = "Anthropic (Claude)"
        elif provider == "deepseek":
            key_name = "DEEPSEEK_API_KEY"
            provider_name = "DeepSeek"
        elif provider == "gemini":
            key_name = "GOOGLE_API_KEY"
            provider_name = "Google (Gemini)"
        else:
            raise ValueError(f"Unknown provider: {provider}")

    # Try to get from environment
    api_key = os.getenv(key_name)

    # If not found, prompt user
    if not api_key:
        api_key = input(f"Enter your {provider_name} API key: ").strip()
        if not api_key and provider != "local":  # Allow empty for local
            print(f"Error: No API key provided for {provider_name}")
            sys.exit(1)

    return api_key

def create_agent(provider: str, use_openrouter: bool, model: str = None, api_url: str = None) -> BaseRecursiveThinkingAgent:
    """Create an agent for the specified provider."""
    api_key = get_api_key(provider, use_openrouter)

    if provider == "openai":
        try:
            from openai_agent import OpenAIRecursiveThinkingAgent
        except ImportError:
            raise ImportError("OpenAI agent requires the 'openai' package. Install it with 'pip install openai'.")

        default_model = "gpt-4o" if not use_openrouter else "openai/gpt-4o"
        model = model or default_model
        return OpenAIRecursiveThinkingAgent(
            api_key=api_key,
            model=model if not use_openrouter else None,
            use_openrouter=use_openrouter,
            openrouter_model=model if use_openrouter else None
        )
    elif provider == "claude":
        try:
            from claude_agent import ClaudeRecursiveThinkingAgent
        except ImportError:
            raise ImportError("Claude agent requires the 'anthropic' package. Install it with 'pip install anthropic'.")

        default_model = "claude-3-opus-20240229" if not use_openrouter else "anthropic/claude-3-opus-20240229"
        model = model or default_model
        return ClaudeRecursiveThinkingAgent(
            api_key=api_key,
            model=model if not use_openrouter else None,
            use_openrouter=use_openrouter,
            openrouter_model=model if use_openrouter else None
        )
    elif provider == "deepseek":
        try:
            from deepseek_agent import DeepSeekRecursiveThinkingAgent
        except ImportError:
            raise ImportError("DeepSeek agent requires the 'requests' package. Install it with 'pip install requests'.")

        default_model = "deepseek-chat" if not use_openrouter else "deepseek/deepseek-chat"
        model = model or default_model
        return DeepSeekRecursiveThinkingAgent(
            api_key=api_key,
            model=model if not use_openrouter else None,
            use_openrouter=use_openrouter,
            openrouter_model=model if use_openrouter else None
        )
    elif provider == "gemini":
        try:
            from gemini_agent import GeminiRecursiveThinkingAgent
        except ImportError:
            raise ImportError("Gemini agent requires the 'google-genai' package. Install it with 'pip install google-genai'.")

        default_model = "gemini-1.5-pro" if not use_openrouter else "google/gemini-1.5-pro"
        model = model or default_model
        return GeminiRecursiveThinkingAgent(
            api_key=api_key,
            model=model if not use_openrouter else None,
            use_openrouter=use_openrouter,
            openrouter_model=model if use_openrouter else None
        )
    elif provider == "local":
        try:
            from local_lm_agent import LocalLMStudioAgent
        except ImportError:
            raise ImportError("Local LM Studio agent requires the 'requests' package. Install it with 'pip install requests'.")

        default_api_url = "http://localhost:1234/v1"
        api_url = api_url or default_api_url
        default_openrouter_model = "openai/gpt-3.5-turbo" if use_openrouter else None
        return LocalLMStudioAgent(
            api_url=api_url,
            model=model,
            use_openrouter=use_openrouter,
            openrouter_api_key=api_key,
            openrouter_model=model or default_openrouter_model
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")

def main():
    """Main function to run the recursive thinking agents."""
    parser = argparse.ArgumentParser(description="Recursive Thinking Agents")
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "claude", "deepseek", "gemini", "local"],
        default="openai",
        help="The LLM provider to use"
    )
    parser.add_argument(
        "--openrouter",
        action="store_true",
        help="Use OpenRouter instead of native API"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model to use (provider-specific if not using OpenRouter)"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        help="API URL for local LM Studio (default: http://localhost:1234/v1)"
    )
    parser.add_argument(
        "--alternatives",
        type=int,
        default=3,
        help="Number of alternative responses to generate in each round (default: 3)"
    )
    # Removed explicit markdown saving parameters - now happens automatically

    args = parser.parse_args()

    print("🤖 Recursive Thinking Agent")
    print("=" * 50)

    # Print configuration
    print(f"Provider: {args.provider}")
    print(f"Using OpenRouter: {args.openrouter}")
    if args.model:
        print(f"Model: {args.model}")
    if args.api_url:
        print(f"API URL: {args.api_url}")
    print("=" * 50)

    # Create the agent
    agent = create_agent(args.provider, args.openrouter, args.model, args.api_url)

    print("\nAgent initialized! Type 'exit' to quit, 'save' to save conversation.")
    print("Type 'save md' to save the last response as markdown.")
    print("The AI will think recursively before each response.\n")

    # Print configuration
    print(f"Number of alternatives per round: {args.alternatives}")
    print(f"Auto-saving responses as markdown to folder: 'responses'")
    print()

    # Keep track of the last result for markdown saving
    last_user_input = None
    last_result = None

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'save':
            agent.save_conversation()
            continue
        elif user_input.lower() == 'save full':
            agent.save_full_log()
            continue
        elif user_input.lower() == 'save md':
            if last_user_input and last_result:
                agent.save_response_as_markdown(last_user_input, last_result, "responses")
            else:
                print("No response to save yet.")
            continue
        elif not user_input:
            continue

        # Get response with thinking process
        result = agent.think_and_respond(user_input, num_alternatives=args.alternatives)

        # Save for later use
        last_user_input = user_input
        last_result = result

        # Display the final response prominently
        print("\n" + "=" * 80)
        print("🤖 AI FINAL RESPONSE:")
        print("=" * 80)
        print(f"{result['response']}")
        print("=" * 80 + "\n")

        # Always show complete thinking process
        print("\n--- COMPLETE THINKING PROCESS ---")
        for item in result['thinking_history']:
            print(f"\nRound {item['round']} {'[SELECTED]' if item['selected'] else '[ALTERNATIVE]'}:")
            print(f"  Response: {item['response']}")
            if 'explanation' in item and item['selected']:
                print(f"  Reason for selection: {item['explanation']}")
            print("-" * 50)
        print("--------------------------------\n")

        # Always auto-save as markdown
        agent.save_response_as_markdown(user_input, result, "responses")

    # Save on exit
    save_on_exit = input("Save conversation before exiting? (y/n): ").strip().lower()
    if save_on_exit == 'y':
        agent.save_conversation()
        save_full = input("Save full thinking log? (y/n): ").strip().lower()
        if save_full == 'y':
            agent.save_full_log()

    print("Goodbye! 👋")

if __name__ == "__main__":
    main()
