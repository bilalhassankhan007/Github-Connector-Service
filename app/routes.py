from fastapi import APIRouter, Query

from app.github_service import GitHubService
from app.schemas import CreateIssueRequest, CreatePullRequestRequest

router = APIRouter()
github_service = GitHubService()


@router.get("/repos")
async def get_repositories(
    owner: str = Query(..., min_length=1),
    owner_type: str = Query("user", pattern="^(user|org)$"),
):
    repos = await github_service.fetch_repositories(owner=owner, owner_type=owner_type)
    return {
        "success": True,
        "data": repos,
    }


@router.post("/create-issue")
async def create_issue(payload: CreateIssueRequest):
    issue = await github_service.create_issue(
        owner=payload.owner,
        repo=payload.repo,
        title=payload.title,
        body=payload.body,
    )
    return {
        "success": True,
        "data": issue,
    }


@router.get("/list-issues")
async def list_issues(
    owner: str = Query(..., min_length=1),
    repo: str = Query(..., min_length=1),
    state: str = Query("open", pattern="^(open|closed|all)$"),
):
    issues = await github_service.list_issues(owner=owner, repo=repo, state=state)
    return {
        "success": True,
        "data": issues,
    }


@router.post("/create-pr")
async def create_pull_request(payload: CreatePullRequestRequest):
    pr = await github_service.create_pull_request(
        owner=payload.owner,
        repo=payload.repo,
        title=payload.title,
        head=payload.head,
        base=payload.base,
        body=payload.body,
    )
    return {
        "success": True,
        "data": pr,
    }


@router.get("/commits")
async def get_commits(
    owner: str = Query(..., min_length=1),
    repo: str = Query(..., min_length=1),
):
    commits = await github_service.fetch_commits(owner=owner, repo=repo)
    return {
        "success": True,
        "data": commits,
    }
