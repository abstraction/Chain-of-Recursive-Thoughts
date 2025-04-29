#!/usr/bin/env python
"""
Wrapper script to run the recursive thinking agents from the root directory.
This simply imports and runs the main function from the custom directory.
"""

import sys
import os

# Add the custom directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom'))

# Import and run the main function from the custom directory
try:
    from recursive_thinking_agents import main
    main()
except ImportError as e:
    print(f"Error importing module: {e}")
    print("\nMake sure you have installed the required dependencies:")
    print("  pip install openai  # For OpenAI")
    print("  pip install anthropic  # For Claude")
    print("  pip install google-genai  # For Gemini")
    print("  pip install requests  # For all agents")
    sys.exit(1)
