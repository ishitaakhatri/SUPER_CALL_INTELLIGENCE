# tools/llm.py

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_agent_suggestion(transcript, member_data, knowledge_docs):

    system_prompt = """
You are an AI agent assist system for a superannuation call center.
Be professional, compliant, and concise.
Mention tax or eligibility if relevant.
"""

    user_prompt = f"""
Transcript:
{transcript}

Member Data:
{member_data}

Relevant Policies:
{knowledge_docs}

Generate a suggested response for the agent.
"""

    response = await client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content
