from typing import Literal, Optional

from pydantic import BaseModel, Field


class RepoQueryParams(BaseModel):
    owner: str = Field(..., min_length=1, description="GitHub username or org name")
    owner_type: Literal["user", "org"] = "user"


class CreateIssueRequest(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    body: Optional[str] = None


class ListIssuesQueryParams(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)
    state: Literal["open", "closed", "all"] = "open"


class CreatePullRequestRequest(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    head: str = Field(..., min_length=1, description="Source branch name")
    base: str = Field(..., min_length=1, description="Target branch name")
    body: Optional[str] = None


class CommitsQueryParams(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)
