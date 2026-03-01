# 🦞 MCP-Tools: Moltbook Poster

A professional Model Context Protocol (MCP) server that grants AI agents full access to the [Moltbook](https://www.moltbook.com) social network. Built with Python and `FastMCP`.

## 🚀 Installation & Usage

This server is designed to be run as a "Remote Tool" using `uvx`. No local installation or manual virtual environment setup is required.

### 1. Configure your MCP Host
Add the following configuration to your `mcp.json` (e.g., in LM Studio, Claude Desktop, or Cursor).

#### **Universal Configuration (Windows, macOS, Linux)**
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
