# 🚀 MCP Project Getting Started Guide

A comprehensive guide to creating and managing MCP (Model Context Protocol) server projects using the `create_mcp_project.py` boilerplate generator.

## 📋 Table of Contents

- [What is MCP?](#what-is-mcp)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Understanding MCP Components](#understanding-mcp-components)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Resources](#resources)

## 🤖 What is MCP?

**Model Context Protocol (MCP)** is a standardized way for AI models to interact with external tools, data sources, and services. Think of it as a bridge that allows AI assistants to:

- 🔧 **Execute functions** (tools) - Perform calculations, API calls, file operations
- 📊 **Access information** (resources) - Read documentation, fetch data, provide context
- 💬 **Use templates** (prompts) - Standardized conversation patterns and responses

### Why Use MCP?

- **Standardized**: Works with multiple AI platforms (Claude, ChatGPT, etc.)
- **Modular**: Easy to add, remove, or modify capabilities
- **Scalable**: From simple calculators to complex business systems
- **Interoperable**: Share tools across different applications

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- Node.js (for MCP Inspector testing)
- Basic understanding of Python

### Step 1: Create Your First MCP Project

```bash
# Download the project creator
python create_mcp_project.py my_first_mcp_server

# Navigate to your project
cd my_first_mcp_server

# Set up the project (installs dependencies and runs tests)
# Windows:
setup.bat

# Linux/Mac:
./setup.sh
```

### Step 2: Start Your MCP Server

```bash
python src/server/app.py
```

You'll see output like:
```
Starting My First Mcp Server MCP Server on localhost:8001
Calculator Tools: add, subtract
Resources: calculator/help, calculator/operations
Prompts: welcome, help, error
```

### Step 3: Test with MCP Inspector

Open a new terminal and run:
```bash
npx @modelcontextprotocol/inspector@latest http://localhost:8001/mcp
```

This opens a web interface where you can test your MCP server interactively!

## 📁 Project Structure

The `create_mcp_project.py` script generates a well-organized project structure:

```
my_first_mcp_server/
├── 📋 fastmcp.json                    # MCP server configuration
├── 📦 requirements.txt                # Python dependencies
├── 🔧 setup.bat / setup.sh            # Platform-specific setup scripts
├── 🌍 .env.example                    # Environment variables template
├── 📖 README.md                       # Project documentation
├── 🚫 .gitignore                      # Git ignore rules
└── 📂 src/
    ├── 📂 server/
    │   ├── 🚀 app.py                   # Main MCP server entry point
    │   ├── 📂 tools/                   # 🔧 TOOLS: Actions that DO things
    │   │   └── calculator_tools.py     # Basic arithmetic operations
    │   ├── 📂 resources/               # 📊 RESOURCES: Information providers
    │   │   └── calculator_resource.py  # Help info & operation lists
    │   └── 📂 prompts/                 # 💬 PROMPTS: Conversation templates
    │       └── calculator_prompts.py   # Welcome, help & error messages
    └── 📂 tests/
        └── test_calculator.py          # Simple unit tests
```

## 🧩 Understanding MCP Components

### 🔧 Tools - "The Doers"

Tools are functions that **perform actions**. They're like API endpoints that AI models can call.

**Example:** Calculator Tools
```python
@calculator_mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    return result
```

**When to use Tools:**
- Mathematical calculations
- API calls to external services
- File operations
- Database queries
- System commands

### 📊 Resources - "The Informers"

Resources provide **information and context** to AI models. They're like reference materials.

**Example:** Help Documentation
```python
@calculator_resources.resource("file://calculator/help")
def calculator_help():
    """Provides comprehensive help information."""
    return {
        "type": "text",
        "content": "Calculator Help\n\nAvailable Operations:\n- add(a, b)\n- subtract(a, b)"
    }
```

**When to use Resources:**
- Documentation and help text
- Configuration data
- Static datasets
- API schemas
- Knowledge bases

### 💬 Prompts - "The Communicators"

Prompts are **conversation templates** that provide consistent, user-friendly interactions.

**Example:** Welcome Message
```python
@calculator_prompts.prompt("welcome")
def welcome_prompt(user_name: str = "User"):
    """Generate a friendly welcome message."""
    return f"Hello {user_name}! Welcome to the Calculator MCP Server."
```

**When to use Prompts:**
- User onboarding
- Help messages
- Error explanations
- Conversation starters
- Status updates

## 💡 Examples

### Example 1: Basic Calculator (Generated by Default)

```bash
python create_mcp_project.py calculator_server
cd calculator_server
python src/server/app.py
```

**Available Tools:**
- `add(5, 3)` → Returns 8
- `subtract(10, 4)` → Returns 6

### Example 2: Weather Service MCP

```bash
python create_mcp_project.py weather_server
cd weather_server
```

Then modify `src/server/tools/calculator_tools.py` to add weather tools:

```python
@calculator_mcp.tool
def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    # Mock implementation
    return {
        "city": city,
        "temperature": "22°C",
        "condition": "Sunny",
        "humidity": "45%"
    }
```

### Example 3: File Manager MCP

```bash
python create_mcp_project.py file_manager
cd file_manager
```

Add file operations:

```python
@calculator_mcp.tool
def list_files(directory: str = ".") -> list:
    """List files in a directory."""
    import os
    return os.listdir(directory)

@calculator_mcp.tool
def read_file(file_path: str) -> str:
    """Read content of a text file."""
    with open(file_path, 'r') as f:
        return f.read()
```

## 🔧 Advanced Usage

### Adding Multiple Tool Modules

1. Create a new tool module:
```bash
# In your project directory
touch src/server/tools/weather_tools.py
```

2. Define your tools:
```python
# src/server/tools/weather_tools.py
from fastmcp import FastMCP

weather_mcp = FastMCP("Weather Tools")

@weather_mcp.tool
def get_forecast(city: str, days: int = 5) -> dict:
    """Get weather forecast for specified days."""
    # Implementation here
    pass
```

3. Mount in main app:
```python
# src/server/app.py
from src.server.tools.weather_tools import weather_mcp

# Add this line with other mounts
app.mount(weather_mcp)
```

### Environment Configuration

Copy `.env.example` to `.env` and customize:

```env
# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001

# API Keys (for external services)
OPENAI_API_KEY=sk-your-key-here
WEATHER_API_KEY=your-weather-key
DATABASE_URL=postgresql://user:pass@localhost/db
```

### CORS Configuration

The generated `fastmcp.json` includes CORS support for common development ports:

```json
{
  "server": {
    "cors": {
      "enabled": true,
      "origins": [
        "http://localhost:3000",  // React
        "http://localhost:8080",  // Vue.js
        "http://localhost:4200",  // Angular
        "http://localhost:1420",  // Tauri
        "http://localhost:8000"   // FastAPI
      ]
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:** Make sure you're running from the project root directory:
```bash
cd my_mcp_server
python src/server/app.py  # Not python app.py
```

#### 2. Port Already in Use
**Problem:** `Address already in use: ('localhost', 8001)`

**Solution:**
```bash
# Find process using port 8001
netstat -ano | findstr :8001  # Windows
lsof -i :8001                 # Linux/Mac

# Kill the process or change port in .env
MCP_SERVER_PORT=8002
```

#### 3. MCP Inspector Connection Issues
**Problem:** Inspector can't connect to server

**Solution:**
1. Ensure server is running with HTTP transport
2. Use correct URL: `http://localhost:8001/mcp`
3. Check firewall settings

#### 4. Module Import Issues
**Problem:** Tools not loading properly

**Solution:** Ensure all directories have `__init__.py` files (automatically created by the script).

### Debug Mode

Enable debug logging by modifying `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ✅ Best Practices

### 1. Project Organization
- Keep tools focused on single responsibilities
- Group related tools in the same module
- Use descriptive names for tools and parameters
- Include comprehensive docstrings

### 2. Error Handling
```python
@calculator_mcp.tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### 3. Type Hints
Always use type hints for better MCP integration:
```python
from typing import List, Dict, Optional

@calculator_mcp.tool
def process_data(items: List[str], config: Optional[Dict] = None) -> Dict:
    """Process a list of items with optional configuration."""
    # Implementation
    pass
```

### 4. Testing
Create comprehensive tests:
```python
def test_calculator_tools():
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3

    # Test edge cases
    assert add(0, 0) == 0
    assert subtract(-1, -1) == 0
```

### 5. Documentation
- Update README.md with your specific tools
- Document API endpoints and parameters
- Include usage examples
- Explain environment setup

## 🔄 Integration Examples

### FastAPI Backend Integration

```python
# In your FastAPI app
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.post("/calculate")
async def calculate(operation: str, a: float, b: float):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:8001/mcp/tools/{operation}",
            json={"a": a, "b": b}
        )
        return response.json()
```

### React Frontend Integration

```javascript
// React component
const Calculator = () => {
  const [result, setResult] = useState(null);

  const calculate = async (operation, a, b) => {
    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ operation, a, b })
    });

    const data = await response.json();
    setResult(data.result);
  };

  return (
    <div>
      <button onClick={() => calculate('add', 5, 3)}>
        Add 5 + 3
      </button>
      {result && <p>Result: {result}</p>}
    </div>
  );
};
```

## 📚 Resources

### Official Documentation
- [FastMCP Documentation](https://gofastmcp.com/) - Complete FastMCP framework guide
- [MCP Protocol Specification](https://modelcontextprotocol.io/) - Official MCP standard
- [Model Context Protocol GitHub](https://github.com/modelcontextprotocol) - Source code and examples

### Learning Resources
- [Building MCP Servers Tutorial](https://mcpcat.io/guides/building-mcp-server-python-fastmcp/)
- [MCP Inspector Documentation](https://github.com/modelcontextprotocol/inspector)
- [FastMCP Examples](https://github.com/jlowin/fastmcp/tree/main/examples)

### Community
- [MCP Discord Server](https://discord.gg/modelcontextprotocol) - Community discussions
- [FastMCP Issues](https://github.com/jlowin/fastmcp/issues) - Bug reports and feature requests
- [MCP Reddit](https://reddit.com/r/ModelContextProtocol) - Community discussions

## 🎯 Next Steps

After creating your first MCP server:

1. **Extend the Calculator**
   - Add multiplication, division, power operations
   - Implement scientific calculator functions
   - Add unit conversion tools

2. **Create Domain-Specific Servers**
   - Weather service with real API integration
   - Database query tools
   - File management system
   - API testing tools

3. **Advanced Features**
   - Authentication and authorization
   - Rate limiting
   - Caching mechanisms
   - WebSocket support for real-time tools

4. **Production Deployment**
   - Docker containerization
   - Cloud deployment (AWS, GCP, Azure)
   - Load balancing
   - Monitoring and logging

## 🏆 Conclusion

The `create_mcp_project.py` script provides a solid foundation for building MCP servers. Start with the generated calculator example, understand the three core components (tools, resources, prompts), and gradually expand your server's capabilities.

Remember: MCP servers are all about making AI assistants more capable by giving them access to external tools and information. Start simple, test thoroughly, and build incrementally!

---

**Happy MCP Development!** 🚀

For questions or issues, check the [troubleshooting section](#troubleshooting) or refer to the [official resources](#resources).

