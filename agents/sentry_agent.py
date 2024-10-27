import os
import requests

from langchain_core.tools import tool
from .agent import Agent


@tool
def sentry_list_issues(project: str) -> str:
    """Returns a formatted string with a list of issues for a given project in Sentry"""
    sentry_url = os.getenv("SENTRY_HTTP_URL", "http://127.0.0.1:9000")
    sentry_organization_slug = os.getenv("SENTRY_ORGANIZATION_SLUG", "sentry")
    auth_token = os.getenv("SENTRY_AUTH_TOKEN", False)
    if not auth_token:
        return "Error: Please set SENTRY_AUTH_TOKEN."

    try:
        # Sentry API endpoint
        url = (
            f"{sentry_url}/api/0/projects/{sentry_organization_slug}/{project}/issues/"
        )

        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

        # Parameters for the request
        params = {
            "statsPeriod": "14d",
        }

        # Make the GET request to Sentry API
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Process the response
        data = response.json()
        if not data:
            return "No issues found."

        # Format the list of issues
        formatted_issues = "List of Sentry Issues:\n"
        for issue in data:
            formatted_issues += f"ID: {issue['id']}, Title: {issue['title']}\n"

        # Return the formatted string
        return formatted_issues
    except requests.RequestException as e:
        return f"Error fetching issues from Sentry: {e}"
    except (KeyError, ValueError) as e:
        return f"Error processing Sentry response: {e}"


@tool
def sentry_get_issue(issue_id: int) -> str:
    """Retrieve detailed information about a specific issue from a Sentry project."""
    sentry_url = os.getenv("SENTRY_HTTP_URL", "http://127.0.0.1:9000")
    auth_token = os.getenv("SENTRY_AUTH_TOKEN", False)
    if not auth_token:
        return "Error: Please set SENTRY_AUTH_TOKEN."
    try:
        issue_id = int(issue_id)
    except ValueError:
        return f"Error: Issue ID {issue_id} wrong format."
    try:
        # Sentry API endpoint for issue details
        issue_url = f"{sentry_url}/api/0/issues/{issue_id}/"

        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

        # Make the GET request to Sentry API for issue details
        issue_response = requests.get(issue_url, headers=headers)
        issue_response.raise_for_status()

        # Process the issue response
        issue_data = issue_response.json()

        # Fetch the latest event for this issue
        events_url = f"{sentry_url}/api/0/issues/{issue_id}/events/latest/"
        event_response = requests.get(events_url, headers=headers)
        event_response.raise_for_status()

        # Process the event response
        event_data = event_response.json()

        # Extract traceback
        traceback = (
            event_data.get("entries", [{}])[0]
            .get("data", {})
            .get("values", [{}])[0]
            .get("stacktrace", {})
            .get("frames", [])
        )

        # Format the issue data
        formatted_data = "Issue Details:\n"
        formatted_data += f"ID: {issue_data['id']}\n"
        formatted_data += f"Title: {issue_data['title']}\n"
        formatted_data += f"Level: {issue_data['level']}\n"
        formatted_data += f"Project: {issue_data['project']['slug']}\n"
        formatted_data += f"First Seen: {issue_data['firstSeen']}\n"
        formatted_data += f"Last Seen: {issue_data['lastSeen']}\n"
        formatted_data += f"Count: {issue_data['count']}\n"
        formatted_data += f"User Count: {issue_data['userCount']}\n"
        formatted_data += f"URL: {issue_data['permalink']}\n"
        formatted_data += "\nLatest Event:\n"
        formatted_data += f"Event ID: {event_data['eventID']}\n"
        formatted_data += f"Timestamp: {event_data['dateCreated']}\n"
        formatted_data += f"Release: {event_data.get('release', 'N/A')}\n"
        formatted_data += "\nTraceback:\n"
        for frame in traceback:
            formatted_data += f"File: {frame.get('filename', 'N/A')}\n"
            formatted_data += f"Line: {frame.get('lineNo', 'N/A')}\n"
            formatted_data += f"Function: {frame.get('function', 'N/A')}\n"
            formatted_data += "Context:\n"
            context = frame.get("context", [])
            for line_num, line_content in context:
                formatted_data += f"{line_num:4d} | {line_content}\n"
            formatted_data += "-" * 50 + "\n"
        return formatted_data

    except requests.RequestException as e:
        return f"Error fetching data from Sentry: {e}"
    except (KeyError, ValueError, IndexError) as e:
        return f"Error processing Sentry response: {e}"


sentry_agent = Agent(
    name="Sentry Agent",
    instructions="""You are a helpful assistant.""",
    functions={
        "sentry_list_issues": sentry_list_issues,
        "sentry_get_issue": sentry_get_issue,
    },
)
