# Changelog

All notable changes to the Recursive Thinking Agents project will be documented in this file.

## [1.0.0] - 2024-06-01

### Added
- Initial release with support for multiple LLM providers
- Base recursive thinking agent implementation
- OpenAI agent with native API and OpenRouter support
- Claude agent with native API and OpenRouter support
- DeepSeek agent with native API and OpenRouter support
- Command-line interface for easy usage
- Example scripts demonstrating each agent
- Comprehensive documentation

### Features
- Recursive thinking process that improves responses through iterative refinement
- Dynamic determination of thinking rounds based on prompt complexity
- Alternative response generation with varying temperatures
- Evaluation and selection of the best response
- Streaming support to see the thinking process in real-time
- Conversation history and thinking logs
- Flexible API options (native or OpenRouter)

## [1.1.0] - 2024-06-02

### Added
- Local LLM agent with LM Studio API support
- Support for running inference on local models
- Improved error handling for all agents
- Additional examples for local model usage

### Changed
- Refactored base agent for better extensibility
- Updated documentation with local LLM usage instructions
- Enhanced streaming output formatting

### Fixed
- Fixed token counting for large responses
- Improved parsing of evaluation responses
- Better handling of API rate limits

## [1.2.0] - 2024-06-03

### Added
- Gemini agent with native API and OpenRouter support
- Increased token limits for all native API implementations
- Improved documentation for all LLM providers
- Additional examples for Gemini usage

### Changed
- Enhanced OpenRouter integration with reasoning parameter
- Updated requirements to include google-generativeai package
- Standardized token limit handling across all providers

### Fixed
- Improved error handling for API-specific issues
- Better handling of model-specific parameters

## [1.3.0] - 2024-06-10

### Changed
- Updated Gemini implementation to use the new `google-genai` library instead of deprecated `google-generativeai`
- Removed `argparse` from requirements.txt as it's a built-in Python module
- Updated API calls in Gemini agent to match the new library's interface

### Fixed
- Fixed compatibility issues with the latest Google Gemini API
- Improved error handling for Gemini API calls
