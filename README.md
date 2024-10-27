# AI Agent Triage System

This project implements a simple AI agent triage system using the Anthropic API and LangChain. It allows users to interact with AI agents to handle various tasks or queries.

## Features

- Utilizes the Anthropic API for natural language processing
- Implements a modular agent system for handling different types of queries
- Currently includes a Sentry agent for retrieving issues

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Anthropic API key: `ANTHROPIC_API_KEY=your_api_key_here`
   - Add your Sentry URL: `SENTRY_HTTP_URL=http://127.0.0.1:9000`
   - Add your Sentry Organization slug: `SENTRY_ORGANIZATION_SLUG=sentry`
   - Add your Sentry Custom Integration TOKEN: `SENTRY_AUTH_TOKEN=XXXX`

## Usage

Run the main script:

```
python run.py
```

You will be prompted to enter queries, which will be processed by the appropriate AI agent.

## Project Structure

- `run.py`: Main entry point of the application
- `agents/agent.py`: Base Agent class definition
- `agents/sentry_agent.py`: Sentry Agent implementation for error monitoring

  - Currently supports retrieving the issues for the last 14 days for a given project name and getting detailed info of an issue given its ID

## Future Improvements

- Implement more specialized agents for different tasks
- Add a selection mechanism to choose the most appropriate agent for each query
- Enhance error handling and logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

