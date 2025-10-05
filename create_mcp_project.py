#!/usr/bin/env python3
"""
FastMCP Server Project Boilerplate Creator
Creates a beginner-friendly MCP server project with tools, resources, and prompts.

Usage:
    python create_mcp_project.py <project_name>

Example:
    python create_mcp_project.py my_mcp_server
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, shell=True):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(command, shell=shell, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None


def create_directory_structure(project_name):
    """Create the MCP project directory structure"""
    base_path = Path(project_name)

    directories = [
        base_path,
        base_path / "src" / "server" / "tools",
        base_path / "src" / "server" / "resources",
        base_path / "src" / "server" / "prompts",
        base_path / "src" / "tests",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    return base_path


def create_file(file_path, content):
    """Create a file with given content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created file: {file_path}")


def create_project_files(base_path, project_name):
    """Create all project files with boilerplate content"""

    # fastmcp.json
    fastmcp_content = f'''{{
  "name": "{project_name}",
  "version": "0.1.0",
  "description": "A beginner-friendly MCP server with basic operations",
  "author": "Your Name",
  "license": "MIT",
  "mcp": {{
    "version": "2024-12-05"
  }},
  "server": {{
    "host": "localhost",
    "port": 8001,
    "cors": {{
      "enabled": true,
      "origins": [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:4200",
        "http://localhost:1420",
        "http://localhost:8000"
      ]
    }}
  }},
  "modules": {{
    "tools": "src.server.tools",
    "resources": "src.server.resources",
    "prompts": "src.server.prompts"
  }}
}}'''

    # requirements.txt
    requirements_content = '''fastmcp>=0.1.0
python-dotenv>=1.0.0
httpx>=0.24.0
pytest>=7.0.0'''

    # .env.example
    env_example_content = '''# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001

# API Keys (optional - for LLM tools)
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
GLM_API_KEY=your-glm-key-here

# Ollama Configuration (local)
OLLAMA_URL=http://localhost:11434'''

    # .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Test
.pytest_cache/
.coverage
htmlcov/'''

    # src/server/app.py
    app_content = f'''"""
{project_name.replace('_', ' ').title()} MCP Server

Main FastMCP instance with tools, resources, and prompts.
"""

import os
from fastmcp import FastMCP
from dotenv import load_dotenv

# Import all modules
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.server.tools.calculator_tools import calculator_mcp
from src.server.resources.calculator_resource import calculator_resources
from src.server.prompts.calculator_prompts import calculator_prompts

# Load environment variables
load_dotenv()

# Create the main MCP server instance
app = FastMCP("{project_name.replace('_', ' ').title()} MCP Server")

# Mount all modules
print("Mounting calculator tools...")
app.mount(calculator_mcp)

print("Mounting calculator resources...")
app.mount(calculator_resources)

print("Mounting calculator prompts...")
app.mount(calculator_prompts)

@app.tool
def get_server_info():
    """Get basic server information."""
    return {{
        "name": "{project_name.replace('_', ' ').title()} MCP Server",
        "version": "0.1.0",
        "tools": ["add", "subtract"],
        "resources": ["calculator/help", "calculator/operations"],
        "prompts": ["welcome", "help", "error"],
        "status": "running"
    }}

if __name__ == "__main__":
    host = os.getenv("MCP_SERVER_HOST", "localhost")
    port = int(os.getenv("MCP_SERVER_PORT", "8001"))

    print(f"Starting {project_name.replace('_', ' ').title()} MCP Server on {{host}}:{{port}}")
    print("Calculator Tools: add, subtract")
    print("Resources: calculator/help, calculator/operations")
    print("Prompts: welcome, help, error")

    # Use HTTP transport for better inspector compatibility
    app.run(transport="http", host=host, port=port, path="/mcp")'''

    # src/server/tools/calculator_tools.py
    tools_content = '''"""
Calculator Tools Module

Contains basic arithmetic operations for demonstration.
"""

from fastmcp import FastMCP

calculator_mcp = FastMCP("Calculator Tools")

@calculator_mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    return result

@calculator_mcp.tool
def subtract(a: float, b: float) -> float:
    """Subtract second number from first number.

    Args:
        a: First number (minuend)
        b: Second number (subtrahend)

    Returns:
        Difference of a - b
    """
    result = a - b
    print(f"Subtracting {a} - {b} = {result}")
    return result'''

    # src/server/resources/calculator_resource.py
    resources_content = '''"""
Calculator Resources Module

Provides information and help content for calculator tools.
"""

from fastmcp import FastMCP

calculator_resources = FastMCP("Calculator Resources")

@calculator_resources.resource("file://calculator/help")
def calculator_help():
    """Provides comprehensive help information about calculator tools."""
    return {
        "type": "text",
        "content": """Calculator Help

Available Operations:
- add(a, b): Add two numbers together
- subtract(a, b): Subtract second number from first

Examples:
- add(5, 3) returns 8
- subtract(10, 4) returns 6

All operations support both integers and floating-point numbers.
        """
    }

@calculator_resources.resource("file://calculator/operations")
def calculator_operations():
    """Lists all available calculator operations with details."""
    return {
        "type": "json",
        "content": {
            "operations": [
                {
                    "name": "add",
                    "description": "Addition operation",
                    "parameters": ["a: number", "b: number"],
                    "return_type": "number",
                    "example": "add(5, 3) → 8"
                },
                {
                    "name": "subtract",
                    "description": "Subtraction operation",
                    "parameters": ["a: number", "b: number"],
                    "return_type": "number",
                    "example": "subtract(10, 4) → 6"
                }
            ],
            "total_operations": 2
        }
    }'''

    # src/server/prompts/calculator_prompts.py
    prompts_content = '''"""
Calculator Prompts Module

Provides conversation templates and user interaction messages.
"""

from fastmcp import FastMCP

calculator_prompts = FastMCP("Calculator Prompts")

@calculator_prompts.prompt("welcome")
def welcome_prompt(user_name: str = "User"):
    """Generate a friendly welcome message for new users."""
    return f"""Hello {user_name}! Welcome to the Calculator MCP Server.

I can help you with basic arithmetic operations:
- Addition: add(a, b)
- Subtraction: subtract(a, b)

Try asking me to add or subtract some numbers!

Example: "Can you add 15 and 27?"
    """

@calculator_prompts.prompt("help")
def help_prompt(operation: str = ""):
    """Provide detailed help and usage instructions."""
    if operation == "add":
        return """Addition Help:

Usage: add(a, b)
- a: First number (any integer or decimal)
- b: Second number (any integer or decimal)
- Returns: Sum of a and b

Examples:
- add(5, 3) = 8
- add(2.5, 1.5) = 4.0
- add(-3, 7) = 4
        """
    elif operation == "subtract":
        return """Subtraction Help:

Usage: subtract(a, b)
- a: First number (minuend)
- b: Second number (subtrahend)
- Returns: Difference of a - b

Examples:
- subtract(10, 3) = 7
- subtract(5.5, 2.5) = 3.0
- subtract(2, 8) = -6
        """
    else:
        return """Calculator Help:

Available commands:
1. add(a, b) - Add two numbers
2. subtract(a, b) - Subtract second from first

For specific help on any operation, ask:
"Help me with addition" or "Help me with subtraction"

All operations work with integers and decimals.
        """

@calculator_prompts.prompt("error")
def error_prompt(error_type: str = "general", details: str = ""):
    """Create user-friendly error messages when things go wrong."""
    if error_type == "invalid_input":
        return f"""Oops! There was an issue with your input.

Problem: {details}

Please make sure you're using numbers only.

Examples of correct usage:
- add(5, 3)
- subtract(10.5, 2.3)

Try again with valid numbers!
        """
    elif error_type == "missing_parameters":
        return """Missing Parameters!

Calculator operations need two numbers.

Correct format:
- add(first_number, second_number)
- subtract(first_number, second_number)

Example: add(5, 3)
        """
    else:
        return f"""Something went wrong!

{details if details else "An unexpected error occurred."}

Please try again or ask for help if the problem persists.
        """'''

    # src/tests/test_calculator.py
    test_content = '''"""
Simple tests for calculator tools
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Define standalone functions for testing (without FastMCP decorators)
def add_test(a: float, b: float) -> float:
    """Add two numbers together for testing."""
    return a + b

def subtract_test(a: float, b: float) -> float:
    """Subtract second number from first for testing."""
    return a - b

def test_add():
    """Test addition function"""
    assert add_test(2, 3) == 5
    assert add_test(-1, 1) == 0
    assert add_test(2.5, 1.5) == 4.0
    print("[PASS] Addition tests passed")

def test_subtract():
    """Test subtraction function"""
    assert subtract_test(5, 3) == 2
    assert subtract_test(1, 1) == 0
    assert subtract_test(2.5, 1.5) == 1.0
    print("[PASS] Subtraction tests passed")

def test_import():
    """Test that modules can be imported successfully"""
    try:
        from src.server.tools.calculator_tools import calculator_mcp
        from src.server.resources.calculator_resource import calculator_resources
        from src.server.prompts.calculator_prompts import calculator_prompts
        print("[PASS] All modules imported successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False

if __name__ == "__main__":
    print("Running calculator tests...")
    test_add()
    test_subtract()
    test_import()
    print("All tests passed!")'''

    # README.md
    readme_content = f'''# {project_name.replace('_', ' ').title()}

A beginner-friendly MCP server with basic calculator operations. Perfect for learning how to build MCP servers with FastMCP!

## 📁 Project Structure

```
{project_name}/
├── fastmcp.json                    # MCP server configuration
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
└── src/
    ├── server/
    │   ├── app.py                  # Main MCP server entry point
    │   ├── tools/                  # 🔧 TOOLS: Actions that DO things
    │   │   └── calculator_tools.py # Add & subtract operations
    │   ├── resources/              # 📊 RESOURCES: Information providers
    │   │   └── calculator_resource.py # Help info & operation lists
    │   └── prompts/                # 💬 PROMPTS: User interaction templates
    │       └── calculator_prompts.py # Welcome, help & error messages
    └── tests/
        └── test_calculator.py      # Simple tests
```

### 📖 Folder Descriptions

**🔧 tools/** - Contains functions that **perform actions**
- These are the main functions your MCP server can execute
- Example: `add(5, 3)` performs addition and returns 8
- Think of tools as "verbs" - they DO something

**📊 resources/** - Contains functions that **provide information**
- These give data and help information to AI models or clients
- Example: List of available operations, help documentation
- Think of resources as "reference materials" - they INFORM

**💬 prompts/** - Contains **conversation templates**
- These provide consistent, friendly messages to users
- Example: Welcome messages, help text, error explanations
- Think of prompts as "scripts" - they help communicate clearly

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd {project_name}
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python src/server/app.py
```

Server starts on: `http://localhost:8001/mcp`

### 3. Inspect the Server (Optional)

Use the official MCP Inspector to test your server interactively:

```bash
npx @modelcontextprotocol/inspector@latest http://localhost:8001/mcp
```

This opens a web interface where you can test all tools, resources, and prompts.

### 4. Test the Tools

```python
# In your application, call the MCP tools:
add(5, 3)        # Returns: 8
subtract(10, 4)  # Returns: 6
```

## 🧮 Available Tools

### `add(a, b)`
Adds two numbers together.

**Example:**
```python
add(5, 3)    # Returns: 8
add(2.5, 1.5) # Returns: 4.0
```

### `subtract(a, b)`
Subtracts the second number from the first.

**Example:**
```python
subtract(10, 3)   # Returns: 7
subtract(5.5, 2.5) # Returns: 3.0
```

### `get_server_info()`
Returns basic server information.

## 📊 Available Resources

### `calculator/help`
Provides help information about calculator tools.

### `calculator/operations`
Lists all available operations with details.

## 💬 Available Prompts

### `welcome`
Generates friendly welcome message for new users.

### `help`
Provides detailed help and usage instructions.

### `error`
Creates user-friendly error messages when things go wrong.

## 🧪 Run Tests

```bash
python src/tests/test_calculator.py
```

## ⚙️ Configuration

Copy `.env.example` to `.env` and customize:

```env
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
```

## 🔗 Integration with FastAPI

```python
# In your FastAPI backend
import httpx

async def call_mcp_add(a: float, b: float):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/mcp/tools/add",
            json={{"a": a, "b": b}}
        )
        return response.json()

# Usage
result = await call_mcp_add(5, 3)  # Returns: {{"result": 8}}
```

## 🌐 CORS Support

The server includes CORS support for:
- React: `http://localhost:3000`
- Vue.js: `http://localhost:8080`
- Angular: `http://localhost:4200`
- Tauri: `http://localhost:1420`
- FastAPI: `http://localhost:8000`

## 📈 Next Steps

To extend this MCP server:

1. **Add more tools** in `calculator_tools.py`:
   ```python
   @calculator_mcp.tool
   def multiply(a, b):
       return a * b
   ```

2. **Create new tool modules** in `src/server/tools/`

3. **Add resources** for data providers

4. **Add prompts** for user interaction

This simple structure follows MCP best practices and can grow with your needs! 🎉

## 📚 Learn More

- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

Perfect starting point for MCP server development! 🚀'''

    # Create __init__.py files
    init_content = ""

    # Create all files
    files_to_create = [
        (base_path / "fastmcp.json", fastmcp_content),
        (base_path / "requirements.txt", requirements_content),
        (base_path / ".env.example", env_example_content),
        (base_path / ".gitignore", gitignore_content),
        (base_path / "README.md", readme_content),
        (base_path / "src" / "__init__.py", init_content),
        (base_path / "src" / "server" / "__init__.py", init_content),
        (base_path / "src" / "server" / "app.py", app_content),
        (base_path / "src" / "server" / "tools" / "__init__.py", init_content),
        (base_path / "src" / "server" / "tools" / "calculator_tools.py", tools_content),
        (base_path / "src" / "server" / "resources" / "__init__.py", init_content),
        (base_path / "src" / "server" / "resources" / "calculator_resource.py", resources_content),
        (base_path / "src" / "server" / "prompts" / "__init__.py", init_content),
        (base_path / "src" / "server" / "prompts" / "calculator_prompts.py", prompts_content),
        (base_path / "src" / "tests" / "__init__.py", init_content),
        (base_path / "src" / "tests" / "test_calculator.py", test_content),
    ]

    for file_path, content in files_to_create:
        create_file(file_path, content)


def create_setup_scripts(base_path):
    """Create platform-specific setup scripts"""

    # Windows setup script
    windows_setup = '''@echo off
echo Setting up MCP Server project...

echo Installing dependencies...
pip install -r requirements.txt

echo Running tests...
python src/tests/test_calculator.py

echo Setup complete!
echo.
echo To run the MCP server:
echo python src/server/app.py
echo.
echo MCP server will be available at: http://localhost:8001/mcp
echo Test with MCP Inspector: npx @modelcontextprotocol/inspector@latest http://localhost:8001/mcp
pause'''

    # Linux/Ubuntu setup script
    linux_setup = '''#!/bin/bash
echo "Setting up MCP Server project..."

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
python src/tests/test_calculator.py

echo "Setup complete!"
echo ""
echo "To run the MCP server:"
echo "python src/server/app.py"
echo ""
echo "MCP server will be available at: http://localhost:8001/mcp"
echo "Test with MCP Inspector: npx @modelcontextprotocol/inspector@latest http://localhost:8001/mcp"'''

    # Create setup scripts
    create_file(base_path / "setup.bat", windows_setup)
    create_file(base_path / "setup.sh", linux_setup)

    # Make Linux script executable
    if platform.system() != "Windows":
        os.chmod(base_path / "setup.sh", 0o755)


def main():
    if len(sys.argv) != 2:
        print("Usage: python create_mcp_project.py <project_name>")
        print("Example: python create_mcp_project.py my_mcp_server")
        sys.exit(1)

    project_name = sys.argv[1]

    if Path(project_name).exists():
        print(f"Error: Directory '{project_name}' already exists!")
        sys.exit(1)

    print(f"Creating MCP Server project: {project_name}")
    print(f"Platform: {platform.system()}")
    print()

    # Create project structure
    base_path = create_directory_structure(project_name)

    # Create all project files
    create_project_files(base_path, project_name)

    # Create setup scripts
    create_setup_scripts(base_path)

    print(f"""
SUCCESS: MCP Server project '{project_name}' created successfully!

Next steps:
  1. cd {project_name}
  2. Run setup script:
     Windows: setup.bat
     Linux:   ./setup.sh
  3. Start the MCP server:
     python src/server/app.py
  4. Test with MCP Inspector:
     npx @modelcontextprotocol/inspector@latest http://localhost:8001/mcp

The MCP server will be available at: http://localhost:8001/mcp
""")


if __name__ == "__main__":
    main()