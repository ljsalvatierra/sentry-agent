from dotenv import load_dotenv

from agents.sentry_agent import sentry_agent
from langchain_anthropic import ChatAnthropic


load_dotenv()


def main():
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=1,
        # other params...
    )
    available_agents = [sentry_agent]
    while True:
        query = input("<Triage Agent> Please enter a query.\n<User> ")
        # TODO: select the best Agent for the current task
        agent = available_agents[0]
        agent.invoke(llm, query)


if __name__ == "__main__":
    main()
