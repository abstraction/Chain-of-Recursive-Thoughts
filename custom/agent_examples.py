"""
Examples of using the recursive thinking agents.

This script demonstrates how to use each of the recursive thinking agents
with both native APIs and OpenRouter.
"""

import os
from openai_agent import OpenAIRecursiveThinkingAgent
from claude_agent import ClaudeRecursiveThinkingAgent
from deepseek_agent import DeepSeekRecursiveThinkingAgent
from gemini_agent import GeminiRecursiveThinkingAgent
from local_lm_agent import LocalLMStudioAgent

def example_openai_native():
    """Example using OpenAI with native API."""
    print("\n=== OpenAI with Native API ===\n")

    # Get API key from environment or user input
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ")

    # Create the agent
    agent = OpenAIRecursiveThinkingAgent(
        api_key=api_key,
        model="gpt-4o",
        use_openrouter=False
    )

    # Get a response
    result = agent.think_and_respond(
        "Explain the concept of recursive thinking in AI in simple terms."
    )

    # Print the final response
    print("\n=== Final Response ===\n")
    print(result["response"])

def example_claude_native():
    """Example using Claude with native API."""
    print("\n=== Claude with Native API ===\n")

    # Get API key from environment or user input
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = input("Enter your Anthropic API key: ")

    # Create the agent
    agent = ClaudeRecursiveThinkingAgent(
        api_key=api_key,
        model="claude-3-opus-20240229",
        use_openrouter=False
    )

    # Get a response
    result = agent.think_and_respond(
        "Write a short poem about artificial intelligence."
    )

    # Print the final response
    print("\n=== Final Response ===\n")
    print(result["response"])

def example_deepseek_native():
    """Example using DeepSeek with native API."""
    print("\n=== DeepSeek with Native API ===\n")

    # Get API key from environment or user input
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        api_key = input("Enter your DeepSeek API key: ")

    # Create the agent
    agent = DeepSeekRecursiveThinkingAgent(
        api_key=api_key,
        model="deepseek-chat",
        use_openrouter=False
    )

    # Get a response
    result = agent.think_and_respond(
        "Explain how to implement a binary search algorithm in Python."
    )

    # Print the final response
    print("\n=== Final Response ===\n")
    print(result["response"])

def example_gemini_native():
    """Example using Gemini with native API."""
    print("\n=== Gemini with Native API ===\n")

    # Get API key from environment or user input
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("Enter your Google API key: ")

    # Create the agent
    agent = GeminiRecursiveThinkingAgent(
        api_key=api_key,
        model="gemini-1.5-pro",
        use_openrouter=False
    )

    # Get a response
    result = agent.think_and_respond(
        "Write a creative short story about artificial intelligence becoming self-aware."
    )

    # Print the final response
    print("\n=== Final Response ===\n")
    print(result["response"])

def example_local_lm_studio():
    """Example using local LM Studio API."""
    print("\n=== Local LM Studio API ===\n")

    # Create the agent with default settings
    agent = LocalLMStudioAgent(
        api_url="http://localhost:1234/v1",
        model=None,  # Model is configured in LM Studio UI
        use_openrouter=False
    )

    # Get a response
    result = agent.think_and_respond(
        "Create a simple Python function to calculate the Fibonacci sequence."
    )

    # Print the final response
    print("\n=== Final Response ===\n")
    print(result["response"])

def example_openrouter():
    """Example using OpenRouter with different models."""
    print("\n=== OpenRouter with Different Models ===\n")

    # Get API key from environment or user input
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenRouter API key: ")

    # Create agents for different models
    openai_agent = OpenAIRecursiveThinkingAgent(
        api_key=api_key,
        use_openrouter=True,
        openrouter_model="openai/gpt-4o"
    )

    claude_agent = ClaudeRecursiveThinkingAgent(
        api_key=api_key,
        use_openrouter=True,
        openrouter_model="anthropic/claude-3-opus-20240229"
    )

    deepseek_agent = DeepSeekRecursiveThinkingAgent(
        api_key=api_key,
        use_openrouter=True,
        openrouter_model="deepseek/deepseek-chat"
    )

    gemini_agent = GeminiRecursiveThinkingAgent(
        api_key=api_key,
        use_openrouter=True,
        openrouter_model="google/gemini-1.5-pro"
    )

    local_agent = LocalLMStudioAgent(
        use_openrouter=True,
        openrouter_api_key=api_key,
        openrouter_model="openai/gpt-3.5-turbo"
    )

    # Get responses from each agent
    prompt = "What are the ethical implications of AI?"

    print("\n--- OpenAI via OpenRouter ---\n")
    openai_result = openai_agent.think_and_respond(prompt)
    print("\n--- Claude via OpenRouter ---\n")
    claude_result = claude_agent.think_and_respond(prompt)
    print("\n--- DeepSeek via OpenRouter ---\n")
    deepseek_result = deepseek_agent.think_and_respond(prompt)
    print("\n--- Gemini via OpenRouter ---\n")
    gemini_result = gemini_agent.think_and_respond(prompt)
    print("\n--- Local LM via OpenRouter ---\n")
    local_result = local_agent.think_and_respond(prompt)

    # Print final responses
    print("\n=== Final Responses ===\n")
    print("OpenAI:", openai_result["response"][:100] + "...")
    print("\nClaude:", claude_result["response"][:100] + "...")
    print("\nDeepSeek:", deepseek_result["response"][:100] + "...")
    print("\nGemini:", gemini_result["response"][:100] + "...")
    print("\nLocal LM:", local_result["response"][:100] + "...")

def main():
    """Main function to run examples."""
    print("Recursive Thinking Agents - Examples")
    print("=" * 50)

    # Ask which example to run
    print("\nWhich example would you like to run?")
    print("1. OpenAI with Native API")
    print("2. Claude with Native API")
    print("3. DeepSeek with Native API")
    print("4. Gemini with Native API")
    print("5. Local LM Studio API")
    print("6. OpenRouter with Different Models")
    print("7. Run All Examples")

    choice = input("\nEnter your choice (1-7): ")

    if choice == "1":
        example_openai_native()
    elif choice == "2":
        example_claude_native()
    elif choice == "3":
        example_deepseek_native()
    elif choice == "4":
        example_gemini_native()
    elif choice == "5":
        example_local_lm_studio()
    elif choice == "6":
        example_openrouter()
    elif choice == "7":
        example_openai_native()
        example_claude_native()
        example_deepseek_native()
        example_gemini_native()
        example_local_lm_studio()
        example_openrouter()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
