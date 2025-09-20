from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web,  send_email, current_time, web_autoopener

load_dotenv(".env")
import os
#print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))
#print("DEBUG GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION, tools=[get_weather, search_web,  send_email, current_time, web_autoopener]) 


# llm agent i need or use 
#voice as per my need i will chnage

async def entrypoint(ctx: agents.JobContext): 
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            api_key="AIzaSyA4c2zJFWmAU3jWoBelGdKNQGzPoi1qKAA",
            voice="Charon",
            temperature=0.8 # Temperature controls creativity vs accuracy:
                            # 0.2–0.4 → serious & deterministic (study/technical)
                            # 0.5–0.7 → balanced, natural flow
                            # 0.8–1.0 → more humor/creativity, sometimes chaotic
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
