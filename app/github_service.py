from typing import Any, Dict, List, Optional

import httpx

from app.config import settings


class GitHubAPIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class GitHubService:
    def __init__(self) -> None:
        self.base_url = settings.GITHUB_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": settings.GITHUB_API_VERSION,
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        timeout = httpx.Timeout(30.0)

        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=timeout,
        ) as client:
            try:
                response = await client.request(
                    method=method,
                    url=endpoint,
                    params=params,
                    json=json_data,
                )
            except httpx.RequestError as exc:
                raise GitHubAPIError(
                    status_code=500,
                    message=f"GitHub API request failed: {str(exc)}",
                ) from exc

        if response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get("message", "GitHub API error")
            except Exception:
                message = response.text or "GitHub API error"

            raise GitHubAPIError(status_code=response.status_code, message=message)

        if response.status_code == 204:
            return None

        return response.json()

    async def fetch_repositories(
        self, owner: str, owner_type: str
    ) -> List[Dict[str, Any]]:
        if owner_type == "org":
            endpoint = f"/orgs/{owner}/repos"
        else:
            endpoint = f"/users/{owner}/repos"

        data = await self._request("GET", endpoint)

        repos = []
        for repo in data:
            repos.append(
                {
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "private": repo["private"],
                    "html_url": repo["html_url"],
                }
            )
        return repos

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: Optional[str] = None,
    ) -> Dict[str, Any]:
        endpoint = f"/repos/{owner}/{repo}/issues"
        payload = {
            "title": title,
            "body": body or "",
        }

        data = await self._request("POST", endpoint, json_data=payload)

        return {
            "id": data["id"],
            "number": data["number"],
            "title": data["title"],
            "state": data["state"],
            "html_url": data["html_url"],
        }

    async def list_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
    ) -> List[Dict[str, Any]]:
        endpoint = f"/repos/{owner}/{repo}/issues"
        params = {"state": state}

        data = await self._request("GET", endpoint, params=params)

        issues_only = []
        for item in data:
            if "pull_request" in item:
                continue

            issues_only.append(
                {
                    "id": item["id"],
                    "number": item["number"],
                    "title": item["title"],
                    "state": item["state"],
                    "html_url": item["html_url"],
                }
            )

        return issues_only

    async def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None,
    ) -> Dict[str, Any]:
        endpoint = f"/repos/{owner}/{repo}/pulls"
        payload = {
            "title": title,
            "head": head,
            "base": base,
            "body": body or "",
        }

        data = await self._request("POST", endpoint, json_data=payload)

        return {
            "id": data["id"],
            "number": data["number"],
            "title": data["title"],
            "state": data["state"],
            "html_url": data["html_url"],
        }

    async def fetch_commits(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        endpoint = f"/repos/{owner}/{repo}/commits"

        data = await self._request("GET", endpoint)

        commits = []
        for item in data:
            commit_info = item.get("commit", {})
            author_info = commit_info.get("author", {})

            commits.append(
                {
                    "sha": item.get("sha"),
                    "message": commit_info.get("message"),
                    "author": author_info.get("name"),
                    "date": author_info.get("date"),
                    "html_url": item.get("html_url"),
                }
            )

        return commits
