from google.genai import types


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


async def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        session = await  session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle the user name
        # user_name = session.state.get("user_name", "Unknown")
        # print(f"👤 User: {user_name}")

        # Handle reminders
        # reminders = session.state.get("reminders", [])
        # if reminders:
        #     print("📝 Reminders:")
        #     for idx, reminder in enumerate(reminders, 1):
        #         print(f"  {idx}. {reminder}")
        # else:
        #     print("📝 Reminders: None")

        
       
        Company_Profile = session.state.get("Company_Profile", "")
        print("vihang")
        print(Company_Profile)
        
        if Company_Profile:
            print("📝 Company_Profile:")
            print(f"  {Company_Profile}")
        else:
            print("📝 Company_Profile: None")

        
    
        
        topic = session.state.get("topic", "")
        if topic:
            print(f"📝 Topic: {topic}")
        else:
            print("📝 Topic: None")
            
        print("-" * (22 + len(label)))
        
    except Exception as e:
        print(f"Error displaying state: {e}")
    

async def process_agent_response(event):
    """Process and display agent response events."""
    final_response = None
    
    # Check for content in any event, not just final ones
    if event.content and event.content.parts:
        for part in event.content.parts:
            # Handle different part types
            if hasattr(part, "text") and part.text and not part.text.isspace():
                text_content = part.text.strip()
                if text_content:  # Only store non-empty responses
                    final_response = text_content
                    print(f"Text: '{text_content}'")
            
            # Handle other part types
            elif hasattr(part, "executable_code") and part.executable_code:
                print(f"Debug: Agent generated code:\n``````")
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                print(f"Debug: Code Execution Result: {part.code_execution_result.outcome}")
            elif hasattr(part, "tool_response") and part.tool_response:
                print(f"Tool Response: {part.tool_response.output}")
    
    # Always return the final response found, regardless of event type
    if final_response:
        print(f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
        print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n")
    
    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}")

    final_response_text = None
    all_responses = []  # Collect all responses as fallback

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                all_responses.append(response)
                final_response_text = response  # Keep updating with latest response
                
    except Exception as e:
        print(f"Error during agent call: {e}")
        return f"Error: {str(e)}"

    # Fallback: return the last non-None response if we have one
    if not final_response_text and all_responses:
        final_response_text = all_responses[-1]
    
    # Final fallback
    if not final_response_text:
        final_response_text = "No response received from agent"
    
    return final_response_text
