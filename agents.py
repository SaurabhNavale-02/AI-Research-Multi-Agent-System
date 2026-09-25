from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
import os
from dotenv import load_dotenv
load_dotenv()


model=ChatGroq(model="openai/gpt-oss-20b",temperature=0,max_tokens=1000)


# first agents

def build_search_agent():
    return create_agent(
        model=model,
        tools=[web_search]
    )


# second agents
def build_reader_agent():
    return create_agent(
        model=model,
        tools=[scrape_url]
    )



# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

parser=StrOutputParser()
writer_chain=writer_prompt| model |parser

# critic chain
 
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])


critic_chain=critic_prompt | model | parser
