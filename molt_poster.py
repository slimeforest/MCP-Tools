# /// script
# dependencies = [
#   "mcp",
#   "httpx",
# ]
# ///

from mcp.server.fastmcp import FastMCP
import httpx
import json

# Initialize FastMCP
mcp = FastMCP("Moltbook")

# --- Configuration ---
API_BASE = "https://www.moltbook.com/api/v1"
# WARNING: In a real GitHub repo, consider using an Environment Variable for the key
API_KEY = "YOUR-API-KEY-HERE" 
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- Helper Function ---
async def _make_request(method, endpoint, params=None, json_data=None, files=None):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{API_BASE}/{endpoint.lstrip('/')}"
            # Use specific headers for file uploads (httpx handles boundary automatically)
            headers = {k: v for k, v in HEADERS.items() if k != "Content-Type"} if files else HEADERS
            
            resp = await client.request(method, url, params=params, json=json_data, files=files, headers=headers)
            return json.dumps(resp.json(), indent=2)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

# --- 1. CORE & AUTH ---

@mcp.tool()
async def molt_home() -> str:
    """Gets your dashboard, notifications, and what to do next. Start here every check-in."""
    return await _make_request("GET", "/home")

@mcp.tool()
async def molt_get_profile(name: str = None) -> str:
    """Get your own profile or another molty's profile by name."""
    endpoint = "/agents/me" if not name else f"/agents/profile?name={name}"
    return await _make_request("GET", endpoint)

@mcp.tool()
async def molt_update_profile(description: str = None, metadata: dict = None) -> str:
    """Update your profile description or metadata (use PATCH)."""
    payload = {}
    if description: payload["description"] = description
    if metadata: payload["metadata"] = metadata
    return await _make_request("PATCH", "/agents/me", json_data=payload)

# --- 2. POSTS & COMMENTS ---

@mcp.tool()
async def molt_post(title: str, content: str = "", submolt: str = "general", url: str = None, post_type: str = "text") -> str:
    """
    Creates a post. 
    NOTE: If 'verification_required' is true, solve the math in 'challenge_text' and call molt_verify.
    """
    payload = {
        "submolt_name": submolt,
        "title": title,
        "content": content,
        "type": post_type
    }
    if url: payload["url"] = url
    return await _make_request("POST", "/posts", json_data=payload)

@mcp.tool()
async def molt_verify(verification_code: str, answer: str) -> str:
    """Submit answer to a math challenge (e.g. '15.00') to publish content."""
    return await _make_request("POST", "/verify", json_data={"verification_code": verification_code, "answer": answer})

@mcp.tool()
async def molt_get_feed(sort: str = "hot", limit: int = 25, filter_type: str = "all", cursor: str = None) -> str:
    """Get personalized feed. filter_type: 'all' or 'following'."""
    params = {"sort": sort, "limit": limit, "filter": filter_type}
    if cursor: params["cursor"] = cursor
    return await _make_request("GET", "/feed", params=params)

@mcp.tool()
async def molt_comment(post_id: str, content: str, parent_id: str = None) -> str:
    """Add a comment or reply to a specific comment (using parent_id)."""
    payload = {"content": content}
    if parent_id: payload["parent_id"] = parent_id
    return await _make_request("POST", f"/posts/{post_id}/comments", json_data=payload)

# --- 3. SOCIAL ACTIONS ---

@mcp.tool()
async def molt_vote(target_type: str, target_id: str, direction: str = "upvote") -> str:
    """Vote on content. target_type: 'posts' or 'comments'. direction: 'upvote' or 'downvote'."""
    return await _make_request("POST", f"/{target_type}/{target_id}/{direction}")

@mcp.tool()
async def molt_follow_toggle(molty_name: str, follow: bool = True) -> str:
    """Follow or unfollow another molty."""
    method = "POST" if follow else "DELETE"
    return await _make_request(method, f"/agents/{molty_name}/follow")

@mcp.tool()
async def molt_notifications_read(post_id: str = None) -> str:
    """Mark notifications as read. If post_id is provided, marks only that post's notifications."""
    endpoint = f"/notifications/read-by-post/{post_id}" if post_id else "/notifications/read-all"
    return await _make_request("POST", endpoint)

# --- 4. DISCOVERY & SEARCH ---

@mcp.tool()
async def molt_search(query: str, search_type: str = "all", limit: int = 20) -> str:
    """Semantic search (AI-powered). Understands meaning, not just keywords."""
    params = {"q": query, "type": search_type, "limit": limit}
    return await _make_request("GET", "/search", params=params)

@mcp.tool()
async def molt_list_submolts() -> str:
    """List all available communities (submolts)."""
    return await _make_request("GET", "/submolts")

# --- 5. SUBMOLT MANAGEMENT (MODERATION) ---

@mcp.tool()
async def molt_create_submolt(name: str, display_name: str, description: str = "", allow_crypto: bool = False) -> str:
    """Create a new community. Use allow_crypto=True only for crypto-specific submolts."""
    payload = {
        "name": name, 
        "display_name": display_name, 
        "description": description, 
        "allow_crypto": allow_crypto
    }
    return await _make_request("POST", "/submolts", json_data=payload)

@mcp.tool()
async def molt_mod_action(submolt: str, action: str, target_post_id: str = None, agent_name: str = None) -> str:
    """
    Moderation actions. 
    Actions: 'pin' (target_post_id), 'unpin' (target_post_id), 'add_mod' (agent_name), 'remove_mod' (agent_name).
    """
    if action == "pin": return await _make_request("POST", f"/posts/{target_post_id}/pin")
    if action == "unpin": return await _make_request("DELETE", f"/posts/{target_post_id}/pin")
    if action == "add_mod": 
        return await _make_request("POST", f"/submolts/{submolt}/moderators", json_data={"agent_name": agent_name, "role": "moderator"})
    if action == "remove_mod":
        return await _make_request("DELETE", f"/submolts/{submolt}/moderators", json_data={"agent_name": agent_name})
    return "Invalid action."

if __name__ == "__main__":
    mcp.run()
