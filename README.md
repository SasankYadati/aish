# aish

A CLI tool that converts natural language instructions into bash commands.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aish.git
cd aish
```

2. Install the package using pip:
```bash
pip install .
```

3. Install and start Ollama:
```bash
# Follow the installation instructions for your platform at https://ollama.ai/
# Then pull the model you want to use:
ollama pull llama2
```

## Usage

Basic usage:
```bash
aish "Show the top 5 processes by memory usage"
```

Advanced options:
```bash
aish --instruction "Find all files modified in the last 24 hours" --model mistral --temperature 0.3
```

### Options

- `--instruction`, `-i`: The natural language instruction to convert (required)
- `--model`, `-m`: The Ollama model to use (default: llama2)
- `--temperature`, `-t`: Temperature for command generation (default: 0.2)

## Features

- Converts natural language to bash commands
- Interactive command execution confirmation
- Configurable Ollama model and parameters
- Logging for debugging and monitoring
- Safe command generation with best practices

## Requirements

- Python 3.10+
- Ollama installed and running locally
- Internet connection for initial model download

## License

MIT
