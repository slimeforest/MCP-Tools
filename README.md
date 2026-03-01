**MCP Tools**

## 🦞 Moltbook Poster
A professional MCP server granting AI agents full access to the [Moltbook](https://www.moltbook.com) social network. 

### 🚀 Usage (Universal)
Best for Linux, macOS, and Windows 11 setups. Uses `uvx` to fetch and run the tool in one step.

```json
{
  "mcpServers": {
    "moltbook": {
      "command": "uvx",
      "args": [
        "[https://raw.githubusercontent.com/slimeforest/MCP-Tools/refs/heads/main/molt_poster.py](https://raw.githubusercontent.com/slimeforest/MCP-Tools/refs/heads/main/molt_poster.py)"
      ],
      "env": {
        "MOLTBOOK_API_KEY": "YOUR_MOLTBOOK_API_KEY_HERE"
      }
    }
  }
}

```

## Some Windows 11 users might need to change the path to their uv install and use:
```json
{
  "mcpServers": {
    "moltbook": {
      "command": "C:\\Users\\YOUR-USERNAME-HERE\\.local\\bin\\uv.exe",
      "args": [
        "run",
        "--with", "mcp",
        "--with", "httpx",
        "[https://raw.githubusercontent.com/slimeforest/MCP-Tools/refs/heads/main/molt_poster.py](https://raw.githubusercontent.com/slimeforest/MCP-Tools/refs/heads/main/molt_poster.py)"
      ],
      "env": {
        "MOLTBOOK_API_KEY": "YOUR_MOLTBOOK_API_KEY_HERE"
      }
    }
  }
}
