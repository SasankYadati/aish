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

3. Install [ollama](https://ollama.com/download)


4. Pull fine-tuned model from ollama:
```bash
ollama pull hf.co/saisasanky/Llama-3.1-8B-Instruct-4bit-aish_gguf
```

## Usage

Basic usage:
```bash
aish "Show the top 5 processes by memory usage"
```

Advanced options:
```bash
aish "Find all files modified in the last 24 hours" --model mistral --temperature 0.3
```

### Options

- `--model`, `-m`: The Ollama model to use (default: llama2)
- `--temperature`, `-t`: Temperature for command generation (default: 0.2)

## Requirements

- Python 3.10+
- Ollama installed and running locally
- Internet connection for initial model download

## License

MIT
