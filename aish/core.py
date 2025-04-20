"""Core functionality for generating bash commands from natural language."""

import logging

import ollama

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)

def generate_command(
    instruction: str,
    model: str = "llama2",
    temperature: float = 0.2,
) -> str:
    """Generate a bash command from a natural language instruction.
    
    Args:
        instruction: The natural language instruction to convert
        model: The Ollama model to use for command generation
        temperature: The temperature parameter for command generation
        
    Returns:
        The generated bash command
        
    Raises:
        ValueError: If the instruction is empty
        ollama.ResponseError: If there's an error with the Ollama API
    """
    if not instruction.strip():
        raise ValueError("Instruction cannot be empty")
    
    # Create the user message
    user_message = f"Convert this instruction to a bash command: {instruction}"
    
    try:
        # Make the API call
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": user_message},
            ],
            options={
                "temperature": temperature,
                "num_predict": 150,
            }
        )
        
        # Extract and clean the command
        command = response['message']['content'].strip()
        
        # Remove any markdown code block formatting if present
        if command.startswith("```bash"):
            command = command[7:]
        if command.startswith("```"):
            command = command[3:]
        if command.endswith("```"):
            command = command[:-3]
            
        return command.strip()
        
    except Exception as e:
        raise ollama.ResponseError(f"Ollama API error: {e!s}") 