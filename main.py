# """
# main.py — stateless runner for Content-Studio
# • Sessions live only in RAM (InMemorySessionService)  
# • Artifacts are still persisted (GCS if bucket set, otherwise in-memory)
# """

# import asyncio, os
# from dotenv import load_dotenv

# from google.adk.runners   import Runner
# from google.adk.sessions  import InMemorySessionService              # ← NEW
# from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService

# from Content_Studio.agent import root_agent
# from utils import call_agent_async

# load_dotenv()

# # ────────────────────────────────────────────────────────────────
# # 1.  Session service ‑- in-memory, wiped when the app exits
# # ────────────────────────────────────────────────────────────────
# session_service = InMemorySessionService()            # sessions are *not* saved to disk[12]

# # ────────────────────────────────────────────────────────────────
# # 2.  Artifact service  (GCS → if bucket set, else in-memory)
# # ────────────────────────────────────────────────────────────────
# gcs_bucket = os.getenv("GCS_ARTIFACT_BUCKET")
# if gcs_bucket:
#     artifact_service = GcsArtifactService(bucket_name=gcs_bucket)
#     print(f"✅ Using GCS bucket “{gcs_bucket}” for artifact storage")
# else:
#     artifact_service = InMemoryArtifactService()
#     print("⚠️  No GCS bucket configured — falling back to in-memory artifacts")

# # ────────────────────────────────────────────────────────────────
# # 3.  Main event loop
# # ────────────────────────────────────────────────────────────────
# async def main_async() -> None:
#     APP_NAME  = "Content-Studio"
#     USER_ID   = "Company_Strategist"

#     # Always start a fresh session — no DB lookup / resume
#     session = await session_service.create_session(
#         app_name = APP_NAME,
#         user_id  = USER_ID,
#         state    = {}                                   # empty initial state[11]
#     )
#     SESSION_ID = session.id
#     print(f"🔄  New ephemeral session: {SESSION_ID}")

#     runner = Runner(
#         agent            = root_agent,
#         app_name         = APP_NAME,
#         session_service  = session_service,
#         artifact_service = artifact_service            # image artifacts still work
#     )

#     print("\nWelcome to Content-Studio!  (type 'exit' to quit)\n")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in {"exit", "quit"}:
#             print("👋  Goodbye.")
#             break
#         await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


# if __name__ == "__main__":
#     asyncio.run(main_async())

"""
main.py â€” stateless runner for Content-Studio
â€¢ Sessions live only in RAM (InMemorySessionService)  
â€¢ Artifacts are still persisted (GCS if bucket set, otherwise in-memory)
"""

import asyncio, os
from dotenv import load_dotenv

from google.adk.runners   import Runner
from google.adk.sessions  import InMemorySessionService              # â† NEW
from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService

from Content_Studio.agent import root_agent
from utils import call_agent_async

load_dotenv()

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  Setup for Streamlit UI integration
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
USER_ID = "Company_Strategist"
APP_NAME = "Content-Studio"
SESSION_ID = None
runner = None

def init_ui_runner():
    global SESSION_ID, runner
    # Create a fresh session for UI
    session = asyncio.run(session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state={}
    ))
    SESSION_ID = session.id
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        artifact_service=artifact_service
    )
session_service = InMemorySessionService() 
# Initialize the runner at import time for UI

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# 1.  Session service â€‘- in-memory, wiped when the app exits
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
           # sessions are *not* saved to disk[12]

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# 2.  Artifact service  (GCS â†’ if bucket set, else in-memory)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
gcs_bucket = os.getenv("GCS_ARTIFACT_BUCKET")
if gcs_bucket:
    artifact_service = GcsArtifactService(bucket_name=gcs_bucket)
    print(f"âœ… Using GCS bucket â€œ{gcs_bucket}â€ for artifact storage")
else:
    artifact_service = InMemoryArtifactService()
    print("âš ï¸  No GCS bucket configured â€” falling back to in-memory artifacts")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# 3.  Main event loop
init_ui_runner()

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
async def main_async() -> None:
    APP_NAME  = "Content-Studio"
    USER_ID   = "Company_Strategist"

    # Always start a fresh session â€” no DB lookup / resume
    session = await session_service.create_session(
        app_name = APP_NAME,
        user_id  = USER_ID,
        state    = {}                                   # empty initial state[11]
    )
    SESSION_ID = session.id
    print(f"ðŸ”„  New ephemeral session: {SESSION_ID}")

    runner = Runner(
        agent            = root_agent,
        app_name         = APP_NAME,
        session_service  = session_service,
        artifact_service = artifact_service            # image artifacts still work
    )

    print("\nWelcome to Content-Studio!  (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("ðŸ‘‹  Goodbye.")
            break
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())
