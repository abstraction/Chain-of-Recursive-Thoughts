# Recursive Thinking Agents 🧠🔄

This package provides implementations of the Chain of Recursive Thoughts (CoRT) technique for multiple LLM providers.

## Supported LLM Providers

- **OpenAI** (GPT-4o, etc.)
- **Claude** (Claude 3 Opus, etc.)
- **DeepSeek** (DeepSeek Chat)
- **Gemini** (Gemini 1.5 Pro, etc.)
- **Local LM Studio** (Run models locally)

## Features

- **Recursive thinking process** - Makes LLMs think harder by generating alternatives and evaluating them
- **Dual API support** - Use either native APIs or OpenRouter
- **Streaming responses** - See the AI's thinking process in real-time
- **Conversation history** - Save and load conversations
- **Thinking logs** - Detailed logs of the thinking process

## Installation

```bash
pip install -r requirements.txt
```

This will install all required dependencies, including:
- `openai` - For OpenAI API
- `anthropic` - For Claude API
- `google-genai` - For Gemini API
- `requests` - For HTTP requests

## Environment Variables

You can set these environment variables or provide them when prompted:

- `OPENAI_API_KEY` - For OpenAI API
- `ANTHROPIC_API_KEY` - For Claude API
- `DEEPSEEK_API_KEY` - For DeepSeek API
- `GOOGLE_API_KEY` - For Gemini API
- `OPENROUTER_API_KEY` - For OpenRouter (works with all models)

Note: Local LM Studio doesn't require an API key when using the local API.

## Usage

### Command Line

```bash
# Use OpenAI with native API
python recursive_thinking_agents.py --provider openai

# Use Claude with OpenRouter
python recursive_thinking_agents.py --provider claude --openrouter

# Use DeepSeek with a specific model
python recursive_thinking_agents.py --provider deepseek --model deepseek-coder

# Use Gemini with native API
python recursive_thinking_agents.py --provider gemini

# Use Gemini with OpenRouter
python recursive_thinking_agents.py --provider gemini --openrouter

# Use Local LM Studio
python recursive_thinking_agents.py --provider local

# Use Local LM Studio with custom API URL
python recursive_thinking_agents.py --provider local --api-url http://localhost:5000/v1
```

### In Your Code

```python
from openai_agent import OpenAIRecursiveThinkingAgent
from claude_agent import ClaudeRecursiveThinkingAgent
from deepseek_agent import DeepSeekRecursiveThinkingAgent
from gemini_agent import GeminiRecursiveThinkingAgent
from local_lm_agent import LocalLMStudioAgent

# Create an OpenAI agent with native API
openai_agent = OpenAIRecursiveThinkingAgent(
    api_key="your-openai-api-key",
    model="gpt-4o"
)

# Create a Claude agent with OpenRouter
claude_agent = ClaudeRecursiveThinkingAgent(
    api_key="your-openrouter-api-key",
    use_openrouter=True,
    openrouter_model="anthropic/claude-3-opus-20240229"
)

# Create a Gemini agent with native API
gemini_agent = GeminiRecursiveThinkingAgent(
    api_key="your-google-api-key",
    model="gemini-1.5-pro"
)

# Create a Local LM Studio agent
local_agent = LocalLMStudioAgent(
    api_url="http://localhost:1234/v1",
    model=None  # Model is configured in LM Studio UI
)

# Get a response with recursive thinking
result = openai_agent.think_and_respond("Explain quantum computing")
print(result["response"])
```

## How It Works

1. The agent determines how many thinking rounds are needed
2. It generates an initial response
3. For each thinking round:
   - Generates alternative responses
   - Evaluates all responses
   - Selects the best one
4. The final response is returned

## Saving Conversations

During a chat session, you can:
- Type `save` to save the conversation history
- Type `save full` to save the full thinking log
- Type `exit` to quit

## Extending

To add support for a new LLM provider:

1. Create a new class that inherits from `BaseRecursiveThinkingAgent`
2. Implement the `_call_api` method
3. Add the provider to the `create_agent` function in `recursive_thinking_agents.py`

## License

MIT - See LICENSE file for details
