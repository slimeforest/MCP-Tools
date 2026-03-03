**MCP Tools**

## 🦞 Moltbook Poster
A professional MCP server granting AI agents full access to the [Moltbook](https://www.moltbook.com) social network. 

### 🚀 Usage (Universal)
Best for Linux, macOS, and Windows 11 setups.

```json
"moltbook": {
  "command": "uv",
  "args": [
    "run",
    "https://raw.githubusercontent.com/slimeforest/MCP-Tools/refs/heads/main/molt_poster.py"
  ],
  "env": {
    "MOLTBOOK_API_KEY": "YOUR_MOLTBOOK_API_KEY_HERE"
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
        "https://raw.githubusercontent.com/slimeforest/MCP-Tools/refs/heads/main/molt_poster.py"
      ],
      "env": {
        "MOLTBOOK_API_KEY": "YOUR_MOLTBOOK_API_KEY_HERE"
      }
    }
  }
}
```

---

## 🎲 Dice Roller
A lightweight MCP server that allows AI agents to roll dice for D&D, tabletop games, or random calculations.

### 🚀 Usage (Universal)

```json
"dice": {
  "command": "uv",
  "args": [
    "run",
    "--with",
    "mcp",
    "https://raw.githubusercontent.com/slimeforest/MCP-Tools/main/dice_roll.py"
  ]
}
```

## Some Windows 11 users might need to change the path to their uv install and use:

```json
{
  "mcpServers": {
    "dice": {
      "command": "C:\\Users\\YOUR-USERNAME-HERE\\.local\\bin\\uv.exe",
      "args": [
        "run",
        "--with", "mcp",
        "https://raw.githubusercontent.com/slimeforest/MCP-Tools/main/dice_roll.py"
      ]
    }
  }
}
```
