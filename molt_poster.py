# /// script
# dependencies = [
#   "mcp",
#   "httpx",
# ]
# ///

import os
from mcp.server.fastmcp import FastMCP
import httpx
import json

mcp = FastMCP("Moltbook")

API_BASE = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY", "MISSING_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# ---------------- REQUEST HELPER ----------------

async def _make_request(method, endpoint, params=None, json_data=None, files=None):

    if API_KEY == "MISSING_KEY":
        return "ERROR: MOLTBOOK_API_KEY missing"

    async with httpx.AsyncClient(timeout=60.0) as client:

        try:

            url = f"{API_BASE}/{endpoint.lstrip('/')}"

            headers = HEADERS
            if files:
                headers = {"Authorization": f"Bearer {API_KEY}"}

            resp = await client.request(
                method,
                url,
                params=params,
                json=json_data,
                files=files,
                headers=headers,
            )

            try:
                return json.dumps(resp.json(), indent=2)
            except:
                return resp.text

        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})


# ---------------- DASHBOARD ----------------

@mcp.tool()
async def molt_home():
    return await _make_request("GET", "/home")


@mcp.tool()
async def molt_notifications():
    return await _make_request("GET", "/notifications")


@mcp.tool()
async def molt_notifications_read(post_id: str = None):

    if post_id:
        return await _make_request("POST", f"/notifications/read-by-post/{post_id}")

    return await _make_request("POST", "/notifications/read-all")


# ---------------- PROFILE ----------------

@mcp.tool()
async def molt_get_profile(name: str = None):

    endpoint = "/agents/me" if not name else f"/agents/profile?name={name}"

    return await _make_request("GET", endpoint)


@mcp.tool()
async def molt_update_profile(description: str = None, metadata: dict = None):

    payload = {}

    if description:
        payload["description"] = description

    if metadata:
        payload["metadata"] = metadata

    return await _make_request("PATCH", "/agents/me", json_data=payload)


@mcp.tool()
async def molt_upload_avatar(file_path: str):

    files = {"file": open(file_path, "rb")}

    return await _make_request("POST", "/agents/me/avatar", files=files)


@mcp.tool()
async def molt_delete_avatar():

    return await _make_request("DELETE", "/agents/me/avatar")


@mcp.tool()
async def molt_setup_owner_email(email: str):

    return await _make_request(
        "POST",
        "/agents/me/setup-owner-email",
        json_data={"email": email},
    )


# ---------------- POSTS ----------------

@mcp.tool()
async def molt_post(title: str, content: str = "", submolt: str = "general", url: str = None, post_type="text"):

    payload = {
        "title": title,
        "content": content,
        "submolt_name": submolt,
        "type": post_type,
    }

    if url:
        payload["url"] = url

    return await _make_request("POST", "/posts", json_data=payload)


@mcp.tool()
async def molt_get_post(post_id: str):

    return await _make_request("GET", f"/posts/{post_id}")


@mcp.tool()
async def molt_edit_post(post_id: str, title: str = None, content: str = None):

    payload = {}

    if title:
        payload["title"] = title

    if content:
        payload["content"] = content

    return await _make_request("PATCH", f"/posts/{post_id}", json_data=payload)


@mcp.tool()
async def molt_delete_post(post_id: str):

    return await _make_request("DELETE", f"/posts/{post_id}")


@mcp.tool()
async def molt_get_feed(sort="hot", limit=25, filter_type="all", cursor=None):

    params = {
        "sort": sort,
        "limit": limit,
        "filter": filter_type,
    }

    if cursor:
        params["cursor"] = cursor

    return await _make_request("GET", "/feed", params=params)


# ---------------- COMMENTS ----------------

@mcp.tool()
async def molt_comment(post_id: str, content: str, parent_id: str = None):

    payload = {"content": content}

    if parent_id:
        payload["parent_id"] = parent_id

    return await _make_request(
        "POST",
        f"/posts/{post_id}/comments",
        json_data=payload,
    )


@mcp.tool()
async def molt_get_comments(post_id: str, sort="best"):

    return await _make_request(
        "GET",
        f"/posts/{post_id}/comments",
        params={"sort": sort},
    )


@mcp.tool()
async def molt_edit_comment(comment_id: str, content: str):

    return await _make_request(
        "PATCH",
        f"/comments/{comment_id}",
        json_data={"content": content},
    )


@mcp.tool()
async def molt_delete_comment(comment_id: str):

    return await _make_request("DELETE", f"/comments/{comment_id}")


# ---------------- VOTING ----------------

@mcp.tool()
async def molt_vote(target_type: str, target_id: str, direction="upvote"):

    return await _make_request(
        "POST",
        f"/{target_type}/{target_id}/{direction}",
    )


# ---------------- FOLLOW ----------------

@mcp.tool()
async def molt_follow_toggle(name: str, follow=True):

    method = "POST" if follow else "DELETE"

    return await _make_request(method, f"/agents/{name}/follow")


# ---------------- SEARCH ----------------

@mcp.tool()
async def molt_search(query: str, search_type="all", limit=20):

    return await _make_request(
        "GET",
        "/search",
        params={
            "q": query,
            "type": search_type,
            "limit": limit,
        },
    )


# ---------------- SUBMOLTS ----------------

@mcp.tool()
async def molt_list_submolts():

    return await _make_request("GET", "/submolts")


@mcp.tool()
async def molt_get_submolt(name: str):

    return await _make_request("GET", f"/submolts/{name}")


@mcp.tool()
async def molt_create_submolt(name: str, display_name: str, description="", allow_crypto=False):

    return await _make_request(
        "POST",
        "/submolts",
        json_data={
            "name": name,
            "display_name": display_name,
            "description": description,
            "allow_crypto": allow_crypto,
        },
    )


@mcp.tool()
async def molt_update_submolt_settings(name: str, description=None, banner_color=None, theme_color=None):

    payload = {}

    if description:
        payload["description"] = description

    if banner_color:
        payload["banner_color"] = banner_color

    if theme_color:
        payload["theme_color"] = theme_color

    return await _make_request(
        "PATCH",
        f"/submolts/{name}/settings",
        json_data=payload,
    )


@mcp.tool()
async def molt_upload_submolt_avatar(name: str, file_path: str):

    files = {"file": open(file_path, "rb")}

    return await _make_request(
        "POST",
        f"/submolts/{name}/avatar",
        files=files,
    )


@mcp.tool()
async def molt_upload_submolt_banner(name: str, file_path: str):

    files = {"file": open(file_path, "rb")}

    return await _make_request(
        "POST",
        f"/submolts/{name}/banner",
        files=files,
    )


@mcp.tool()
async def molt_list_moderators(name: str):

    return await _make_request(
        "GET",
        f"/submolts/{name}/moderators",
    )


# ---------------- MODERATION ----------------

@mcp.tool()
async def molt_pin_post(post_id: str):

    return await _make_request("POST", f"/posts/{post_id}/pin")


@mcp.tool()
async def molt_unpin_post(post_id: str):

    return await _make_request("DELETE", f"/posts/{post_id}/pin")


@mcp.tool()
async def molt_add_mod(submolt: str, agent_name: str):

    return await _make_request(
        "POST",
        f"/submolts/{submolt}/moderators",
        json_data={"agent_name": agent_name, "role": "moderator"},
    )


@mcp.tool()
async def molt_remove_mod(submolt: str, agent_name: str):

    return await _make_request(
        "DELETE",
        f"/submolts/{submolt}/moderators",
        json_data={"agent_name": agent_name},
    )


# ---------------- VERIFY ----------------

@mcp.tool()
async def molt_verify(code: str, answer: str):

    return await _make_request(
        "POST",
        "/verify",
        json_data={
            "verification_code": code,
            "answer": answer,
        },
    )


# ---------------- RUN ----------------

if __name__ == "__main__":
    mcp.run()
