# GitHub Connector Service

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Architecture](#3-project-architecture)
4. [Folder & File Structure](#4-folder--file-structure)
5. [File-by-File Summary](#5-file-by-file-summary)
6. [Execution Flow](#6-execution-flow)
7. [API Endpoints](#7-api-endpoints)
8. [Authentication](#8-authentication)
9. [Setup & Configuration](#9-setup--configuration)
10. [Testing & Demonstration](#10-testing--demonstration)
11. [Error Handling](#11-error-handling)
12. [Security Notes](#12-security-notes)
13. [Assignment Coverage](#13-assignment-coverage)
14. [Developer Notes](#14-developer-notes)
15. [Conclusion](#15-conclusion)

---

## 1. Project Overview

### 1.1 Introduction

The **GitHub Connector Service** is a FastAPI-based backend application that securely authenticates with GitHub using a **Personal Access Token (PAT)** and performs real GitHub REST API actions.

This project was built as part of a backend developer assignment to demonstrate:

- **External API integration**
- **Authentication handling**
- **REST endpoint design**
- **Clean and modular Python code**
- **Proper request validation and error handling**

---

### 1.2 Core Features

The service supports the following GitHub operations:

- **Fetch repositories** for a user or organization
- **Create an issue** in a repository
- **List issues** from a repository
- **Create a pull request**
- **Fetch commits** from a repository

---

### 1.3 Objective

The main objective of this project is to build a simple but production-style GitHub connector that:

- securely handles authentication
- makes real API calls to GitHub
- exposes usable backend endpoints
- follows clean code structure

---

### 1.4 Target users / stakeholders

- **Backend Developers** – understand the API integration and extend functionality
- **Reviewers / Interviewers** – evaluate code structure, API design, and implementation quality
- **Future maintainers** – quickly understand project flow and extend the connector
- **Students / Learners** – use this as a reference for FastAPI + GitHub API integration

---

## 2. Technology Stack

### 2.1 Backend

- **Python**
- **FastAPI**

### 2.2 HTTP Client

- **httpx**

### 2.3 Validation

- **Pydantic**

### 2.4 Environment Management

- **python-dotenv**

### 2.5 Development Server

- **Uvicorn**

---

## 3. Project Architecture

### 3.1 High-level architecture description

The system is a **small modular FastAPI backend** with:

- an **API layer** for exposing endpoints
- a **service layer** for GitHub API communication
- a **schema layer** for request validation
- a **configuration layer** for secure token loading

---

### 3.2 Architecture pattern

This project follows a **layered backend structure**:

- **Routes layer** – defines API endpoints
- **Schemas layer** – validates request payloads
- **Service layer** – handles business logic and GitHub API calls
- **Config layer** – loads settings from environment variables

---

### 3.3 Request flow

**Client (Swagger/Postman)**  
→ **FastAPI Route**  
→ **GitHub Service Layer**  
→ **GitHub REST API**  
→ **Response returned to client**

---

## 4. Folder & File Structure

```bash
github-connector-service/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── github_service.py
│   └── routes.py
│
├── requirements.txt
└── .env
```

---

## 5. File-by-File Summary

### 5.1 **main.py**

This is the main entry point of the FastAPI application.
Responsibilities:

- create FastAPI app instance
- register routes
- handle global exceptions
- validate configuration at startup

### 5.2 **config.py**

This file is responsible for environment-based configuration.
Responsibilities:

- load .env
- read GITHUB_TOKEN
- store GitHub base settings
- validate token presence

### 5.3 **schemas.py**

This file contains all request validation models.
Responsibilities:

- validate request payloads
- enforce required fields
- improve API consistency

### 5.4 **github_service.py**

This is the core integration layer.
Responsibilities:

- communicate with GitHub API
- send authenticated requests
- handle GitHub responses
- raise custom API errors

### 5.5 **routes.py**

This file defines all FastAPI endpoints.
Responsibilities:

- expose REST endpoints
- receive query/body input
- call service methods
- return structured responses

---

## 6. Execution Flow

### 6.1 Application startup flow

FastAPI application starts
.env file is loaded
GITHUB_TOKEN is validated
routes are registered
server starts listening for requests

### 6.2 Endpoint execution flow

- For every request:
- client sends request to FastAPI endpoint
- request data is validated using Pydantic
- route calls the GitHub service
- service sends authenticated request to GitHub
- GitHub response is processed
- final response is returned to client

### 6.3 Pull request execution flow

- To create a pull request successfully:
- repository must exist
- base branch must exist
- head branch must exist
- head branch must contain changes
- FastAPI sends request to GitHub PR API
- GitHub creates the pull request and returns PR details

---

## 7. API Endpoints

### 7.1 Fetch repositories

**Method**: GET
**Endpoint**: /repos

**Query Parameters**:

owner → GitHub username or organization name
owner_type → user or org

### 7.2 Create issue

- **Method**: POST
- **Endpoint**: /create-issue

- **Request Body**:
  JSON -
  {
  "owner": "bilalhassankhan007",
  "repo": "MiniStore_Checkout_Platform",
  "title": "Test issue from API",
  "body": "This issue was created using the GitHub Connector Service."
  }

---

### 7.3 List issues

- **Method**: GET
- **Endpoint**: /list-issues

**Query Parameters**:

- owner
- repo
- state → open, closed, or all

### 7.4 Create pull request

- **Method**: POST
- **Endpoint**: /create-pr

JSON:
{
"owner": "bilalhassankhan007",
"repo": "MiniStore_Checkout_Platform",
"title": "Test PR from API",
"head": "feature-branch",
"base": "main",
"body": "This pull request was created using the GitHub Connector Service."
}

**Important Note**:

- head branch must exist
- base branch must exist
- head branch must have changes

### 7.5 Fetch commits

- **Method**: GET
- **Endpoint**: /commits

**Query Parameters**:

- owner
- repo

---

## 8. Authentication

### 8.1 Authentication method used

This project uses **GitHub Personal Access Token (PAT)** authentication.

### 8.2 Token handling

The token is stored securely in the .env file and is **not hardcoded** in the source code.

**Example: (.env)**
GITHUB_TOKEN=your_github_personal_access_token_here

---

## 9. Setup & Configuration

### 9.1 Clone the repository

git clone <your-repository-url>
cd github-connector-service

### 9.2 Create virtual environment

python -m venv .venv
.venv\Scripts\Activate.ps1

### 9.3 Install dependencies

pip install -r requirements.txt

### 9.4 Add GitHub token

Create a .env file in the project root and add:
GITHUB_TOKEN=your_github_personal_access_token_here

### 9.5 Run the application

uvicorn app.main:app --reload

### 9.6 Open Swagger UI

http://127.0.0.1:8000/docs

---

## 10. Testing & Demonstration

### 10.1 Testing tools used

- **The project was tested using:**
- FastAPI Swagger UI
- Postman
- GitHub repository verification

### 10.2 Verified actions

- **The following actions were successfully tested:**
- fetch repositories
- fetch commits
- list issues
- create issue
- create pull request

### 10.3 Demonstration flow

**Recommended demonstration order:**

- show project structure in VS Code
- show secure token setup in .env
- run FastAPI application
- test /repos
- test /commits
- test /list-issues
- test /create-issue
- test /create-pr
- verify issue and PR directly on GitHub

---

## 11. Error Handling

### 11.1 Handled scenarios

**The project includes handling for:**

- missing GitHub token
- invalid request payload
- GitHub authentication errors
- repository not found
- branch validation failure
- general API failures

### 11.2 Example error response

**JSON** -
{
**"success"**: false,
**"error"**: "Validation Failed"
}

---

## 12. Security Notes

### 12.1 Implemented security measures

- token stored in **_.env_**
- no hardcoded credentials
- credentials separated from source code
- token not exposed in API responses

### 12.2 Important precautions

do not commit **_.env_** to GitHub
do not share the token publicly
keep token private after submission

### 12.3 Recommended .gitignore

**.env**
**.venv/** \*/
**pycache**/

---

## 14. Developer Notes

### 14.1 Pull request behavior

- A pull request is created from a head branch into a base branch.
- That is why a separate branch with at least one change was required before testing the /create-pr endpoint.

### 14.2 Branch strategy used

For **PR** testing:

- main was used as the stable base branch
- **feature-branch** was used as the temporary test branch
- one small file was added to create a valid branch difference

### 14.3 Practical note

If the same PR is attempted again for the same unchanged branch comparison, GitHub may return a validation error because the comparison is already used or no longer valid.

---

## 15. Conclusion
The GitHub Connector Service successfully demonstrates a clean FastAPI backend that integrates with GitHub using secure PAT authentication and performs real GitHub REST API operations.

It satisfies the assignment requirements by providing:

- secure authentication
- usable REST endpoints
- real external API calls
- clean code organization
- structured validation and error handling
