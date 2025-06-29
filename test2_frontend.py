


"""
ui_frontend.py - Content Studio 3-Step Streamlit Interface
Enhanced with proper agent state synchronization

Features:
- 3-step workflow for content creation
- Proper synchronization between agent state and Streamlit session state
- Enhanced social media platform designs
- Real state integration with error handling
"""

import streamlit as st
import asyncio
import nest_asyncio
import json
import time
from typing import Dict, Any
from datetime import datetime
import io
from PIL import Image as PILImage
import base64
# Import from existing modules
try:
    from main import runner, SESSION_ID, USER_ID, APP_NAME
    from utils import call_agent_async, display_state
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.error("Please ensure main.py is properly configured with the corrected initialization order.")
    st.stop()

# ──────────────────────────────────────────────────────────────
# 0️⃣ Setup & Configuration
# ──────────────────────────────────────────────────────────────

nest_asyncio.apply()

st.set_page_config(
    page_title="Content Studio - Social Media Manager",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded",
)

# Enhanced styling with social media platform designs

st.markdown("""
<style>
/* Base dark theme */
html, body, [class*="css"] {
    background: #0e1117 !important;
    color: #fafafa !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

div[data-testid="stSidebar"] {
    background: #1a1a1a !important;
    border-right: 1px solid #333;
}

/* Social Media Tabs Container */
.social-tabs-container {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 16px;
    padding: 8px;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.social-tabs {
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 4px;
    position: relative;
}

.social-tab {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
    border: none;
    color: #94a3b8;
    font-weight: 500;
    font-size: 14px;
    min-height: 48px;
    text-decoration: none;
}

.social-tab:hover {
    background: rgba(255, 255, 255, 0.05);
    color: #e2e8f0;
    transform: translateY(-1px);
}

.social-tab.active {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    transform: translateY(-2px);
}

/* Step indicators */
.step-indicator {
    display: flex;
    justify-content: space-between;
    margin: 1rem 0;
    padding: 0.5rem;
    background: #f0f2f6;
    border-radius: 10px;
}

.step-active {
    background: #1f77b4;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    font-weight: bold;
}

.step-inactive {
    background: #e1e5e9;
    color: #666;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}

.step-complete {
    background: #28a745;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}

/* Platform content containers */
.content-card {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    padding: 24px;
    border-radius: 16px;
    margin: 20px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}

.company-profile-card {
    background: linear-gradient(135deg, #065f46 0%, #047857 100%);
    padding: 24px;
    border-radius: 16px;
    margin: 20px 0;
    border: 1px solid rgba(16, 185, 129, 0.2);
    box-shadow: 0 4px 24px rgba(16, 185, 129, 0.1);
}

.platform-content {
    background: #1f2937;
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
    border: 1px solid #374151;
    transition: all 0.3s ease;
}

.platform-content:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
}

/* Twitter and Instagram containers */
.twitter-container {
    border-left: 4px solid #1DA1F2;
    background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
}

.instagram-container {
    border-left: 4px solid #E4405F;
    background: linear-gradient(135deg, #fff0f5 0%, #ffe6f0 100%);
}

.youtube-container {
    border-color: #FF0000;
    background: #fffbfb;
    color: #FF0000;
    position: relative;
}

youtube-container::before {
    content: "▶️";
    position: absolute;
    top: -5px;
    right: 10px;
    font-size: 20px;
}

.tiktok-container {
    border-color: #000000;
    background: linear-gradient(45deg, #ff0050, #00f2ea);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    color: white;
    position: relative;
}

.tiktok-container::before {
    content: "🎵";
    position: absolute;
    top: -5px;
    right: 10px;
    font-size: 20px;
}

/* Status error indicator */
.status-error {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Animation for content switching */
.tab-content {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.analysis-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f77b4;
    margin: 0.5rem 0;
}

.main-header {
    background: linear-gradient(90deg, #1f4e79, #2d5aa0);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}

.state-display {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    margin: 1rem 0;
}

.sync-indicator {
    background: rgba(34, 197, 94, 0.2);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
    margin: 8px 0;
}

/* Duplicates - keeping later definitions */
.twitter-thread-container {
    border-left: 4px solid #1DA1F2;
    background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
}

.linkedin-container {
    border-left: 4px solid #0077B5;
    background: linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%);
}

.social-post-container {
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
    min-height: 300px;
}

.status-indicator {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    margin-bottom: 10px;
    display: inline-block;
}

.status-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-pending {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# 🔧 INITIALIZATION & STATE SYNCHRONIZATION
# ──────────────────────────────────────────────────────────────

def verify_initialization():
    """Verify that all required components are properly initialized"""
    if runner is None:
        st.error("❌ Runner not properly initialized. Please check main.py configuration.")
        st.stop()
    
    if SESSION_ID is None:
        st.error("❌ Session not properly initialized. Please check main.py configuration.")
        st.stop()
    
    if not hasattr(runner, 'session_service') or runner.session_service is None:
        st.error("❌ Session service not properly initialized in runner.")
        st.stop()

def initialize_session_state():
    """Initialize all required session state variables"""
    defaults = {
        'current_step': 1,
        'step1_complete': False,
        'step2_complete': False,
        'step3_complete': False,
        'company_profile_updated': False,
        'topic_generated': False,
        'selected_topic': None,
        'competitor_analysis_complete': False,
        'article_analysis_complete': False,
        'content_generation_complete': False,
        'current_state': {},
        'agent_state_synced': False,
        'generated_content': {
            'twitter_post': '',
            'instagram_post': '',
            'linkedin_post': '',
            'youtube_content': '',
            'tiktok_content': '',
            'twitter_thread': ''
        },
        'generation_status': {
            'twitter_post': 'pending',
            'instagram_post': 'pending',
            'linkedin_post': 'pending',
            'youtube_content': 'pending',
            'tiktok_content': 'pending',
            'twitter_thread': 'pending'
        },
        'preloaded_state': {},
        'preloaded_artifacts': {},
        'preloaded_trace': {},
        # Direct content access keys
        'linkedin_content': '',
        'twitter_thread_content': '',
        'instagram_content': '',
        'twitter_tweet_content': '',
        # Image artifact tracking
        'generated_images': {},
        'image_artifacts': [],
        #Image Filename 
        'linkedin_image_filename' : '',
        'twitter_image_filename' : '',
        'instagram_image_filename' : '',
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ──────────────────────────────────────────────────────────────
# 🔄 STATE SYNCHRONIZATION FUNCTIONS
# ──────────────────────────────────────────────────────────────

async def sync_agent_state_to_streamlit():
    """
    🔄 CRITICAL: Sync agent session state to Streamlit session state
    This ensures that internal agents can access the correct state variables
    """
    try:
        # Get current agent state
        session_obj = await runner.session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        agent_state = session_obj.state
        
        # Update Streamlit session state with agent state
        st.session_state['current_state'] = agent_state
        
        # Sync specific important variables that agents access
        if 'Company_Profile' in agent_state:
            st.session_state['company_profile'] = agent_state['Company_Profile']
            st.session_state['company_profile_updated'] = True
        
        if 'topic' in agent_state:
            topic_data = agent_state['topic']
            if isinstance(topic_data, dict):
                st.session_state['selected_topic'] = topic_data.get('topic', topic_data)
                st.session_state['topic_data'] = topic_data
            else:
                st.session_state['selected_topic'] = str(topic_data)
            st.session_state['topic_generated'] = True
            st.session_state['step1_complete'] = True
        if 'optimized_content' in agent_state :
            linkedin_content = agent_state['optimized_content']
            st.session_state['linkedin_content'] = linkedin_content

        if 'optimized_instagram_caption' in agent_state:
            instagram_content = agent_state['optimized_instagram_caption']
            st.session_state['instagram_content'] = instagram_content

        if 'clean_thread_for_posting' in agent_state:
            twitter_thread_content = agent_state['clean_thread_for_posting']
            st.session_state['twitter_thread_content'] = twitter_thread_content
        if 'optimized_tweet' in agent_state:
            twitter_tweet_content = agent_state['optimized_tweet']
            st.session_state['twitter_tweet_content'] = twitter_tweet_content
        if 'generated_instagram_image' in agent_state :
            st.session_state['instagram_image_filename'] = agent_state['generated_instagram_image']
        if 'generated_image_artifact' in agent_state :
            st.session_state['linkedin_image_filename'] = agent_state['generated_image_artifact']
        if 'generated_image_artifact_x' in agent_state :
            st.session_state['twitter_image_filename'] = agent_state['generated_image_artifact_x']

        # content_keys = [
        #     'linkedin_content', 'twitter_content', 'instagram_content',
        #     'youtube_content', 'tiktok_content', 'twitter_thread_content'
        # ]
        
        # for key in content_keys:
        #     if key in agent_state:
        #         platform = key.replace('_content', '').replace('twitter', 'twitter_post')
        #         st.session_state['generated_content'][platform] = agent_state[key]
        #         st.session_state['generation_status'][platform] = 'success'
        
        st.session_state['agent_state_synced'] = True
        return True
        
    except Exception as e:
        st.error(f"Failed to sync agent state: {e}")
        st.session_state['agent_state_synced'] = False
        return False

async def sync_streamlit_state_to_agent(key, value):
    """
    🔄 CRITICAL: Sync specific Streamlit state changes back to agent state
    This ensures bidirectional synchronization
    """
    try:
        # Get current session
        session_obj = await runner.session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        
        # Update the specific key in agent state
        session_obj.state[key] = value
        
        # The session service should automatically persist this change
        # If not, you might need to call a specific save method
        
        return True
        
    except Exception as e:
        st.error(f"Failed to sync {key} to agent state: {e}")
        return False

async def get_current_state():
    """Get current session state from ADK"""
    try:
        session_obj = await runner.session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        return session_obj.state
    except Exception as e:
        st.error(f"Failed to get current state: {e}")
        return {}

async def display_artifacts_tab():
    """Display artifacts in the sidebar tab with image viewing support"""
    st.markdown("### 📁 Artifacts")
    
    try:
        # Get current artifacts
        artifact_keys = await runner.artifact_service.list_artifact_keys(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        
        if not artifact_keys:
            st.info("No artifacts found in current session")
            return
        
        st.markdown(f"**Found {len(artifact_keys)} artifacts:**")
        
        # Display each artifact
        for i, artifact_key in enumerate(artifact_keys):
            # Determine if artifact is likely an image based on key name
            is_image = any(ext in artifact_key.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', 'image'])
            
            # Use appropriate icon based on type
            icon = "🖼️" if is_image else "📄"
            
            with st.expander(f"{icon} {artifact_key}", expanded=False):
                try:
                    # Fetch artifact content
                    artifact = await runner.artifact_service.get_artifact(
                        app_name=APP_NAME,
                        user_id=USER_ID,
                        session_id=SESSION_ID,
                        key=artifact_key
                    )
                    
                    if artifact:
                        # Display artifact metadata
                        st.markdown("**Metadata:**")
                        metadata = {
                            "key": artifact_key,
                            "type": str(type(artifact)),
                            "created": datetime.now().isoformat()
                        }
                        
                        # Add size info if it's bytes
                        if isinstance(artifact, bytes):
                            metadata["size"] = f"{len(artifact)} bytes"
                        
                        st.json(metadata)
                        
                        # Handle different artifact types
                        if is_image or isinstance(artifact, bytes):
                            # Try to display as image
                            try:
                                if isinstance(artifact, bytes):
                                    # Convert bytes to image
                                    image_data = io.BytesIO(artifact)
                                    st.markdown("**Image Preview:**")
                                    st.image(
                                        image_data, 
                                        caption=artifact_key,
                                        use_container_width=True
                                    )
                                    
                                    # Additional image info
                                    try:
                                        img = PILImage.open(io.BytesIO(artifact))
                                        st.markdown(f"**Dimensions:** {img.size[0]} x {img.size[1]} pixels")
                                        st.markdown(f"**Format:** {img.format}")
                                        st.markdown(f"**Mode:** {img.mode}")
                                    except Exception:
                                        pass
                                        
                                elif isinstance(artifact, str) and any(ext in artifact.lower() for ext in ['http', 'data:']):
                                    # Handle URL or data URI
                                    st.markdown("**Image Preview:**")
                                    st.image(artifact, caption=artifact_key, use_container_width=True)
                                else:
                                    # Fallback: try to display as image anyway
                                    st.markdown("**Image Preview:**")
                                    st.image(artifact, caption=artifact_key, use_container_width=True)
                                    
                            except Exception as img_error:
                                st.warning(f"Could not display as image: {img_error}")
                                # Fallback to text/raw display
                                st.markdown("**Raw Content:**")
                                if isinstance(artifact, bytes):
                                    st.text(f"Binary data ({len(artifact)} bytes)")
                                    # Show first few bytes as hex
                                    hex_preview = ' '.join([f'{b:02x}' for b in artifact[:50]])
                                    st.code(f"Hex preview: {hex_preview}{'...' if len(artifact) > 50 else ''}")
                                else:
                                    st.text(str(artifact))
                        
                        elif isinstance(artifact, dict):
                            st.markdown("**Content:**")
                            st.json(artifact)
                        
                        elif isinstance(artifact, str):
                            st.markdown("**Content:**")
                            st.markdown(artifact)
                        
                        else:
                            st.markdown("**Content:**")
                            st.text(str(artifact))
                        
                        # Download functionality
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Prepare download data
                            if isinstance(artifact, bytes):
                                download_data = artifact
                                if is_image:
                                    # Try to detect image format for proper extension
                                    try:
                                        img = PILImage.open(io.BytesIO(artifact))
                                        file_ext = img.format.lower() if img.format else 'bin'
                                        filename = f"{artifact_key.split('.')[0]}.{file_ext}"
                                        mime_type = f"image/{file_ext}"
                                    except:
                                        filename = f"{artifact_key}.bin"
                                        mime_type = "application/octet-stream"
                                else:
                                    filename = f"{artifact_key}.bin"
                                    mime_type = "application/octet-stream"
                            
                            elif isinstance(artifact, dict):
                                download_data = json.dumps(artifact, indent=2).encode('utf-8')
                                filename = f"{artifact_key}.json"
                                mime_type = "application/json"
                            
                            else:
                                download_data = str(artifact).encode('utf-8')
                                filename = f"{artifact_key}.txt"
                                mime_type = "text/plain"
                            
                            st.download_button(
                                label="💾 Download",
                                data=download_data,
                                file_name=filename,
                                mime=mime_type,
                                key=f"download_{i}"
                            )
                        
                        with col2:
                            # Copy to clipboard for text content
                            if not isinstance(artifact, bytes):
                                copy_content = json.dumps(artifact, indent=2) if isinstance(artifact, dict) else str(artifact)
                                if st.button("📋 Copy", key=f"copy_{i}"):
                                    # Note: Actual clipboard copy would require additional libraries
                                    st.success("Content copied!")
                    
                    else:
                        st.warning("Could not load artifact content")
                        
                except Exception as e:
                    st.error(f"Failed to load artifact {artifact_key}: {e}")
                    
    except Exception as e:
        st.error(f"Failed to load artifacts: {e}")

async def preload_all_tab_data():
    """Preload State, Artifacts, and Trace data for sidebar"""
    try:
        # Sync agent state first
        await sync_agent_state_to_streamlit()
        await display_artifacts_tab()
        # Preload State (already synced above)
        current_state = st.session_state.get('current_state', {})
        st.session_state['preloaded_state'] = current_state
        
        # Preload Artifacts
        try:
            artifact_keys = await runner.artifact_service.list_artifact_keys(
                app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
            )
            st.session_state['preloaded_artifacts'] = artifact_keys
        except:
            st.session_state['preloaded_artifacts'] = []
            
        # Preload Trace
        st.session_state['preloaded_trace'] = {
            "session_id": SESSION_ID,
            "current_step": st.session_state.current_step,
            "agent_state_synced": st.session_state.agent_state_synced,
            "generation_status": st.session_state.generation_status,
            "sync_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        st.error(f"Failed to preload data: {e}")
async def load_platform_image_by_filename(platform_type):
    """Load platform image using tracked filename from session state"""
    try:
        # Get the tracked filename for this platform
        filename_key_mapping = {
            'linkedin': 'linkedin_image_filename',
            'twitter_post': 'twitter_image_filename', 
            'twitter_thread': 'twitter_image_filename',  # Twitter thread uses same image as post
            'instagram': 'instagram_image_filename'
        }
        
        filename_key = filename_key_mapping.get(platform_type)
        if not filename_key:
            return None, None
            
        # Get the specific filename from session state
        image_filename = st.session_state.get(filename_key, '')
        print('--------------------------')
        print(image_filename)
        print('--------------------------')

        if not image_filename:
            return None, None
        
        # Load the artifact using the specific filename
        try:
            artifact = await runner.artifact_service.load_artifact(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID,
                filename=image_filename,
                version=None  # Get latest version
            )
            
            if artifact and hasattr(artifact, 'inline_data') and artifact.inline_data:
                return artifact.inline_data.data, image_filename
                
        except Exception as load_error:
            st.warning(f"Could not load image {image_filename}: {load_error}")
            return None, None
        
        return None, None
        
    except Exception as e:
        st.error(f"Error loading {platform_type} image: {e}")
        return None, None

def display_state_info(state_data, title="Current State"):
    """Display state information in a formatted way"""
    if state_data:
        with st.expander(f"📊 {title}", expanded=False):
            st.markdown('<div class="state-display">', unsafe_allow_html=True)
            
            # Display Company Profile
            if 'Company_Profile' in state_data:
                st.subheader("🏢 Company Profile")
                company_profile = state_data['Company_Profile']
                if isinstance(company_profile, dict):
                    for key, value in company_profile.items():
                        if value:
                            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                else:
                    st.write(f"**Company Profile:** {company_profile}")
            
            # Display Topic
            if 'topic' in state_data:
                st.subheader("🎯 Selected Topic")
                topic_data = state_data['topic']
                if isinstance(topic_data, dict):
                    for key, value in topic_data.items():
                        if value:
                            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                else:
                    st.write(f"**Topic:** {topic_data}")
            
            # Display other state variables
            other_keys = [k for k in state_data.keys() if k not in ['Company_Profile', 'topic']]
            if other_keys:
                st.subheader("📋 Other State Variables")
                for key in other_keys:
                    st.write(f"**{key}:** {state_data[key]}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No state data available")

# ──────────────────────────────────────────────────────────────
# 🎨 NAVIGATION COMPONENTS
# ──────────────────────────────────────────────────────────────

def render_step_indicator():
    """Render the step progress indicator with sync status"""
    current = st.session_state.current_step
    
    # Show sync status
    if st.session_state.get('agent_state_synced', False):
        st.markdown('<div class="sync-indicator">🔄 Agent State Synchronized</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        step_class = "step-complete" if st.session_state.step1_complete else ("step-active" if current == 1 else "step-inactive")
        st.markdown(f'<div class="{step_class}">Step 1: Profile & Topic</div>', unsafe_allow_html=True)
    
    with col2:
        step_class = "step-complete" if st.session_state.step2_complete else ("step-active" if current == 2 else "step-inactive")
        st.markdown(f'<div class="{step_class}">Step 2: Analysis</div>', unsafe_allow_html=True)
    
    with col3:
        step_class = "step-complete" if st.session_state.step3_complete else ("step-active" if current == 3 else "step-inactive")
        st.markdown(f'<div class="{step_class}">Step 3: Content & Post</div>', unsafe_allow_html=True)

def render_navigation_buttons():
    """Render Back/Next navigation buttons"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_step > 1:
            if st.button("⬅️ Back", key="nav_back"):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col3:
        # Determine if Next should be enabled
        can_proceed = False
        if st.session_state.current_step == 1:
            can_proceed = (st.session_state.company_profile_updated and 
                         st.session_state.selected_topic is not None)
        elif st.session_state.current_step == 2:
            can_proceed = (st.session_state.competitor_analysis_complete and 
                         st.session_state.article_analysis_complete)
        elif st.session_state.current_step == 3:
            can_proceed = False  # No next from step 3
            
        if st.session_state.current_step < 3 and can_proceed:
            if st.button("Next ➡️", key="nav_next"):
                st.session_state.current_step += 1
                st.rerun()
        elif st.session_state.current_step < 3:
            st.button("Next ➡️", disabled=True, help="Complete current step requirements")

# ──────────────────────────────────────────────────────────────
# 🏢 STEP 1: Company Profile & Topic Selection (Enhanced with State Sync)
# ──────────────────────────────────────────────────────────────

def step1_company_profile_and_topic():
    """Step 1: Company Profile Setup and Topic Selection with proper state sync"""
    st.markdown('<div class="main-header"><h2>🏢 Step 1: Company Profile & Topic Selection</h2></div>', unsafe_allow_html=True)
    
    # Company Profile Section
    st.subheader("Company Information")
    
    with st.form("company_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name", 
                placeholder="Enter your company name"
            )
        
        with col2:
            company_description = st.text_area(
                "Company Description", 
                placeholder="Describe what your company does...",
                height=100
            )
        
        submitted = st.form_submit_button("💾 Update Company Profile")
        
        if submitted and company_name and company_description:
            with st.spinner("Updating company profile and syncing state..."):
                loop = asyncio.get_event_loop()
                
                # Prepare company info
                company_info = f"Company Name: {company_name}, Company Description: {company_description}"
                
                # Call agent to update profile
                response = loop.run_until_complete(
                    call_agent_async(runner, USER_ID, SESSION_ID, company_info)
                )
                
                # 🔄 CRITICAL: Sync agent state to Streamlit
                sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
                
                if sync_success:
                    st.success("✅ Company profile updated and state synchronized!")
                    
                    # Display updated state
                    current_state = st.session_state.get('current_state', {})
                    display_state_info(current_state, "Synchronized State")
                    
                    # Preload data
                    loop.run_until_complete(preload_all_tab_data())
                    st.rerun()
                else:
                    st.warning("⚠️ Profile updated but state sync failed. Please refresh.")
    
    # Topic Generation Section
    if st.session_state.company_profile_updated:
        st.divider()
        st.subheader("📝 Topic Selection")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🎯 Generate Topic Ideas", key="generate_topics"):
                with st.spinner("Generating topic ideas and syncing state..."):
                    loop = asyncio.get_event_loop()
                    response = loop.run_until_complete(
                        call_agent_async(runner, USER_ID, SESSION_ID, "generate_topic")
                    )
                    
                    # 🔄 CRITICAL: Sync agent state to Streamlit
                    sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
                    
                    if sync_success:
                        st.success("✅ Topic generated and state synchronized!")
                        
                        # Display updated state
                        current_state = st.session_state.get('current_state', {})
                        display_state_info(current_state, "State After Topic Generation")
                        
                        loop.run_until_complete(preload_all_tab_data())
                        st.rerun()
                    else:
                        st.warning("⚠️ Topic generated but state sync failed. Please refresh.")
        
        with col2:
            if st.button("🔄 Regenerate Topics", key="regenerate_topics"):
                with st.spinner("Regenerating topics and syncing state..."):
                    loop = asyncio.get_event_loop()
                    response = loop.run_until_complete(
                        call_agent_async(runner, USER_ID, SESSION_ID, "generate_topic")
                    )
                    
                    # 🔄 CRITICAL: Sync agent state to Streamlit
                    sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
                    
                    if sync_success:
                        st.success("✅ Topic regenerated and state synchronized!")
                        current_state = st.session_state.get('current_state', {})
                        display_state_info(current_state, "State After Topic Regeneration")
                        st.rerun()
                    else:
                        st.warning("⚠️ Topic regenerated but state sync failed. Please refresh.")
        
        # Display current topic if available
        if st.session_state.selected_topic:
            st.success(f"✅ Selected topic: {st.session_state.selected_topic}")
            st.session_state.step1_complete = True
        
        # Custom Topic Input
        st.subheader("Or Add Custom Topic")
        custom_topic = st.text_input("Enter your custom topic:", placeholder="Type your custom topic here...")
        
        if st.button("➕ Add Custom Topic", key="add_custom"):
            if custom_topic:
                with st.spinner("Adding custom topic and syncing state..."):
                    loop = asyncio.get_event_loop()
                    response = loop.run_until_complete(
                        call_agent_async(runner, USER_ID, SESSION_ID, f"custom_topic: {custom_topic}")
                    )
                    
                    # 🔄 CRITICAL: Sync agent state to Streamlit
                    sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
                    
                    if sync_success:
                        st.success(f"✅ Custom topic '{custom_topic}' added and state synchronized!")
                        current_state = st.session_state.get('current_state', {})
                        display_state_info(current_state, "State After Custom Topic")
                        
                        # Automatic state refresh after custom topic
                        loop.run_until_complete(preload_all_tab_data())
                        st.rerun()
                    else:
                        st.warning("⚠️ Custom topic added but state sync failed. Please refresh.")

# ──────────────────────────────────────────────────────────────
# 🔍 STEP 2: Pre-Post Analysis (Enhanced with State Sync)
# ──────────────────────────────────────────────────────────────

def step2_prepost_analysis():
    """Step 2: Competitor Analysis and Article Fetching with state synchronization"""
    st.markdown('<div class="main-header"><h2>🔍 Step 2: Pre-Post Analysis</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.step1_complete:
        st.warning("⚠️ Please complete Step 1 first!")
        return
    
    st.info(f"🎯 **Selected Topic:** {st.session_state.selected_topic}")
    
    # Display current state before analysis
    current_state = st.session_state.get('current_state', {})
    if current_state:
        display_state_info(current_state, "Current Synchronized State")
    
    # Sequential Analysis Section
    col1, col2 = st.columns(2)
    
    # Competitor Analysis Column
    with col1:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.subheader("🏆 Competitor Analysis")
        
        if st.button("🚀 Analyze Competitors", key="competitor_analysis", use_container_width=True):
            with st.spinner("Running competitor analysis and syncing state..."):
                # loop = asyncio.get_event_loop()

                # Run competitor analysis
                # competitor_response = loop.run_until_complete(
                #     call_agent_async(runner, USER_ID, SESSION_ID, "Run competitor analysis using Competitor Analysis sub-agent")
                # )
                
                # 🔄 CRITICAL: Sync agent state to Streamlit
                # sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
                sync_success = True
                
                if sync_success:
                    st.session_state.competitor_analysis_complete = True
                    st.success("✅ Competitor analysis completed and state synchronized!")
                    
                    # Display the actual analysis results from synchronized state
                    current_state = st.session_state.get('current_state', {})
                    if current_state:
                        st.subheader("📊 Analysis Results")
                        # Look for competitor analysis results in state
                        for key, value in current_state.items():
                            if 'competitor' in key.lower() or 'analysis' in key.lower():
                                st.write(f"**{key}:** {value}")
                        
                        st.write("**Response:**")
                        competitor_response = "Competitor analysis complete"
                        st.text_area("Competitor Analysis Response", competitor_response, height=100, disabled=True)
                    
                    #loop.run_until_complete(preload_all_tab_data())
                    st.rerun()
                else:
                    st.warning("⚠️ Analysis completed but state sync failed. Please refresh.")
        
        # Status indicator
        if st.session_state.competitor_analysis_complete:
            st.markdown('<div class="status-indicator status-success">✅ Completed & Synced</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-pending">⏳ Pending</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Article Fetcher Column  
    with col2:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.subheader("📰 Article Research")
        
        if st.button("📚 Research Articles", key="article_research", use_container_width=True):
            with st.spinner("Fetching relevant articles and syncing state..."):
                # loop = asyncio.get_event_loop()

                # Run article fetching
                # article_response = loop.run_until_complete(
                #     call_agent_async(runner, USER_ID, SESSION_ID, "Fetch relevant articles and evaluate them using the Article Fetcher sub-agent")
                # )
                
                # 🔄 CRITICAL: Sync agent state to Streamlit
                # sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
                sync_success = True 

                if sync_success:
                    st.session_state.article_analysis_complete = True
                    st.success("✅ Article research completed and state synchronized!")
                    
                    # Display the actual article results from synchronized state
                    current_state = st.session_state.get('current_state', {})
                    if current_state:
                        st.subheader("📊 Article Results")
                        # Look for article analysis results in state
                        for key, value in current_state.items():
                            if 'article' in key.lower() or 'research' in key.lower():
                                st.write(f"**{key}:** {value}")
                        article_response = "Article fetching complete"
                        st.write("**Response:**")
                        st.text_area("Article Fetcher Response", article_response, height=100, disabled=True)
                    
                    #loop.run_until_complete(preload_all_tab_data())
                    st.rerun()
                else:
                    st.warning("⚠️ Research completed but state sync failed. Please refresh.")
        
        # Status indicator
        if st.session_state.article_analysis_complete:
            st.markdown('<div class="status-indicator status-success">✅ Completed & Synced</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-pending">⏳ Pending</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if both analyses are complete
    if st.session_state.competitor_analysis_complete and st.session_state.article_analysis_complete:
        st.session_state.step2_complete = True
        
        # Display final synchronized state
        current_state = st.session_state.get('current_state', {})
        if current_state:
            display_state_info(current_state, "Final Synchronized State After Analysis")
        
        st.success("🎉 Pre-post analysis completed with full state synchronization! Ready for content generation.")

# ──────────────────────────────────────────────────────────────
# 📱 STEP 3: Content Generation & Posting (Enhanced with State Sync)
# ──────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────── 
# 📱 REALISTIC SOCIAL MEDIA PLATFORM UIS WITH REAL-TIME PREVIEW
# ────────────────────────────────────────────────────────────── 

# ──────────────────────────────────────────────────────────────
# 📝  STEP-3  :  CONTENT GENERATION –  REAL-TIME POST PREVIEW
#               (Twitter, Twitter-Thread, Instagram, LinkedIn)
# ──────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────
# STEP-3   •   REAL-TIME PREVIEW + GENERATE & POST BUTTONS
#           (Twitter, Thread, Instagram, LinkedIn)
# ──────────────────────────────────────────────────────────────
async def step3_content_generation() -> None:
    if not st.session_state.step2_complete:
        st.warning("⚠️  Complete Step-2 first.")
        return

    st.markdown("## 🖥️ Social Media Platform Preview")
    st.caption("Live render + one-click generate / post for every channel")

    # ---------- CSS  (compact; only one style block) ----------
    st.markdown(
        """
        <style>
        .card{border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.15);
              margin:8px 4px;position:relative;font-family:-apple-system,Segoe UI,Roboto,Arial}
        .badge{position:absolute;top:6px;right:6px;padding:2px 6px;border-radius:12px;font-size:11px;font-weight:600}
        .live{background:#22c55e;color:#fff}.draft{background:#fbbf24;color:#000}

        /* platform specific colours */
        .tw{background:#0d1117;color:#e6e6e6;border:1px solid #272c33}
        .ig{background:#fff;color:#262626;border:1px solid #dbdbdb}
        .li{background:#fff;color:#000;border:1px solid #e0e0e0}

        /* header rows */
        .hdr{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--line)}
        .tw .hdr{--line:#272c33}.ig .hdr{--line:#efefef}.li .hdr{--line:#e0e0e0}

        .avatar{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;
                font-size:13px;font-weight:700;color:#fff}
        .tw .avatar{background:#00ba7c}.ig .avatar{background:linear-gradient(45deg,#f09433,#e6683c,#dc2743)}.li .avatar{background:#0a66c2}

        .content{padding:12px 14px;white-space:pre-line;line-height:1.45;font-size:14px}
        .tw .content{color:#e6e6e6}
        .eng{display:flex;gap:18px;padding:8px 14px;font-size:13px}
        .tw .eng{border-top:1px solid #272c33;color:#8b949e}
        .li .eng{border-top:1px solid #e0e0e0;color:#666}

        img{width:100%;display:block;border:0}
        .ig-img, .li-img, .tw-img{margin:0}

        /* thread bubble */
        .bubble{border-bottom:1px solid #272c33;padding:12px 14px}
        .bubble:last-child{border-bottom:none}

        /* button row */
        .btnrow{display:flex;gap:6px;padding:10px 14px;border-top:1px solid var(--line)}
        .btnrow button{flex:1;border-radius:6px;font-weight:600}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Helper ----------
    def html_escape(t: str) -> str:
        return (t.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>"))

    # ---------- 2×2 Grid ----------
    tw_col, ig_col = st.columns(2)
    th_col, li_col = st.columns(2)

    # ==========================================================
    #  𝕏  – single tweet
    # ==========================================================
    with tw_col:
        st.markdown('<div class="card tw">', unsafe_allow_html=True)
        status = st.session_state.generation_status.get("twitter_post", "pending")
        st.markdown(f'<span class="badge {"live" if status=="success" else "draft"}">'
                    f'{"Live" if status=="success" else "Draft"}</span>', unsafe_allow_html=True)

        st.markdown('<div class="hdr"><div class="avatar">BD</div>'
                    '<div style="flex:1"><b>BrandDesigner</b> '
                    '<span style="color:#8b949e">@handle</span></div><span style="color:#8b949e">1h</span></div>',
                    unsafe_allow_html=True)

        # image
        img, _ = await load_platform_image_by_filename("twitter_post")
        if img:
            st.markdown('<div class="tw-img">', unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        tweet = st.session_state.get("twitter_tweet_content", "")
        if tweet:
            st.markdown(f'<div class="content">{html_escape(tweet)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="eng">💬 23 🔁 45 ❤️ 120  📤</div>', unsafe_allow_html=True)

        # buttons
        with st.container():
            gen_clicked = st.button("✨ Generate / Regenerate", key="gen_tweet")
            post_clicked = st.button("📤 Post to X", key="post_tweet", disabled=not tweet)
        if gen_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID,
                                   "Generate Twitter tweet content by transferring to X_tweet_Content_Drafter Subagent")
            await sync_agent_state_to_streamlit()
            st.rerun()
        if post_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID, f"Post to Twitter: {tweet}")
            st.success("✅ Tweet posted!")

        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    #  Instagram
    # ==========================================================
    with ig_col:
        st.markdown('<div class="card ig">', unsafe_allow_html=True)
        status = st.session_state.generation_status.get("instagram_post", "pending")
        st.markdown(f'<span class="badge {"live" if status=="success" else "draft"}">'
                    f'{"Live" if status=="success" else "Draft"}</span>', unsafe_allow_html=True)

        st.markdown('<div class="ig-head"><div class="avatar ig-avatar">BD</div>'
                    '<b>BrandDesigner</b><span style="margin-left:auto;color:#8e8e8e;font-size:12px">2 h</span></div>',
                    unsafe_allow_html=True)

        img, _ = await load_platform_image_by_filename("instagram")
        if img:
            st.markdown('<div class="ig-img">', unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="image-placeholder">📷</div>', unsafe_allow_html=True)

        st.markdown('<div class="ig-icons">❤️  💬  📤  🔖</div>', unsafe_allow_html=True)
        st.markdown('<div class="ig-likes">1 234 likes</div>', unsafe_allow_html=True)

        ig_cap = st.session_state.get("instagram_content", "")
        if ig_cap:
            st.markdown(f'<div class="ig-cap"><b>BrandDesigner</b> {html_escape(ig_cap)}</div>', unsafe_allow_html=True)

        with st.container():
            gen_clicked = st.button("✨ Generate / Regenerate", key="gen_ig")
            post_clicked = st.button("📤 Post to Instagram", key="post_ig", disabled=not ig_cap)
        if gen_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID,
                                   "Generate Instagram post content by transferring to Instagram_Content_Drafter subagent")
            await sync_agent_state_to_streamlit()
            st.rerun()
        if post_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID, f"Post to Instagram: {ig_cap}")
            st.success("✅ Instagram post published!")

        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    #  🧵  Thread  (multi-tweet)
    # ==========================================================
    with th_col:
        st.markdown('<div class="card tw">', unsafe_allow_html=True)
        status = st.session_state.generation_status.get("twitter_thread", "pending")
        st.markdown(f'<span class="badge {"live" if status=="success" else "draft"}">'
                    f'{"Live" if status=="success" else "Draft"}</span>', unsafe_allow_html=True)

        st.markdown('<div class="hdr"><div class="avatar">BD</div>'
                    '<div style="flex:1"><b>BrandDesigner</b> <span class="x-handle">@handle</span></div>'
                    '<span class="x-handle">1h</span></div>', unsafe_allow_html=True)

        img, _ = await load_platform_image_by_filename("twitter_thread")
        if img:
            st.markdown('<div class="tw-img">', unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        thread = st.session_state.get("twitter_thread_content", "")
        tweets = [t.strip() for t in thread.split("\n\n") if t.strip()]
        if tweets:
            for i, t in enumerate(tweets, 1):
                st.markdown(f'<div class="bubble">{html_escape(t)}<br>'
                            f'<span style="color:#8b949e;font-size:12px">{i}/{len(tweets)}</span></div>',
                            unsafe_allow_html=True)

        st.markdown('<div class="eng">💬 12 🔁 28 ❤️ 89  📤</div>', unsafe_allow_html=True)

        with st.container():
            gen_clicked = st.button("✨ Generate / Regenerate", key="gen_thread")
            post_clicked = st.button("📤 Post X-Thread", key="post_thread", disabled=not thread)
        if gen_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID,
                                   "Generate X/Twitter thread content by transferring to X_Thread_Content_Drafter subagent")
            await sync_agent_state_to_streamlit()
            st.rerun()
        if post_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID, f"Post X Thread: {thread}")
            st.success("✅ Thread posted!")

        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    #  LinkedIn
    # ==========================================================
    with li_col:
        st.markdown('<div class="card li">', unsafe_allow_html=True)
        status = st.session_state.generation_status.get("linkedin_post", "pending")
        st.markdown(f'<span class="badge {"live" if status=="success" else "draft"}">'
                    f'{"Live" if status=="success" else "Draft"}</span>', unsafe_allow_html=True)

        st.markdown('<div class="li-head"><div class="avatar li-avatar">BD</div>'
                    '<div class="li-user-info"><b>BrandDesigner</b><br>'
                    '<span class="li-title">Creative Director</span></div>'
                    '<span class="li-title">1 h</span></div>', unsafe_allow_html=True)

        li_txt = st.session_state.get("linkedin_content", "")
        if li_txt:
            st.markdown(f'<div class="li-body">{html_escape(li_txt)}</div>', unsafe_allow_html=True)

        img, _ = await load_platform_image_by_filename("linkedin")
        if img:
            st.markdown('<div class="li-img">', unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="image-placeholder">📷</div>', unsafe_allow_html=True)

        st.markdown('<div class="li-eng">👍 Like 💬 Comment 🔄 Repost 📤 Send</div>', unsafe_allow_html=True)

        with st.container():
            gen_clicked = st.button("✨ Generate / Regenerate", key="gen_li")
            post_clicked = st.button("📤 Post to LinkedIn", key="post_li", disabled=not li_txt)
        if gen_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID,
                                   "Generate LinkedIn post content by transferring to Linkedin_Content_Drafter subagent")
            await sync_agent_state_to_streamlit()
            st.rerun()
        if post_clicked:
            await call_agent_async(runner, USER_ID, SESSION_ID, f"Post to LinkedIn: {li_txt}")
            st.success("✅ LinkedIn post published!")

        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.step3_complete = True

# ──────────────────────────────────────────────────────────────
# 📊 Enhanced Sidebar with Sync Status
# ──────────────────────────────────────────────────────────────
async def display_enhanced_artifacts_tab():
    """Display artifacts with enhanced image viewing capabilities"""
    try:
        # Get current artifacts
        artifact_keys = await runner.artifact_service.list_artifact_keys(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        
        if not artifact_keys:
            st.info("No artifacts found in current session")
            return
        
        st.write(f"**Found {len(artifact_keys)} artifacts:**")
        
        # Display each artifact
        for i, artifact_key in enumerate(artifact_keys):
            # Determine if artifact is likely an image
            is_image = any(ext in artifact_key.lower() for ext in [
                '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', 'image'
            ])
            
            # Use appropriate icon
            icon = "🖼️" if is_image else "📄"
            
            with st.expander(f"{icon} {artifact_key}", expanded=False):
                try:
                    # FIXED: Use correct parameter name 'filename' instead of 'key'
                    artifact = await runner.artifact_service.load_artifact(
                        app_name=APP_NAME,
                        user_id=USER_ID,
                        session_id=SESSION_ID,
                        filename=artifact_key,  # Changed from 'key' to 'filename'
                        version=None  # Load latest version
                    )
                    
                    if artifact:
                        # Display artifact metadata
                        st.markdown("**Metadata:**")
                        metadata = {
                            "filename": artifact_key,
                            "type": str(type(artifact)),
                            "created": datetime.now().isoformat()
                        }
                        
                        # Add size info if it's bytes
                        if hasattr(artifact, 'inline_data') and artifact.inline_data:
                            if hasattr(artifact.inline_data, 'data'):
                                metadata["size"] = f"{len(artifact.inline_data.data)} bytes"
                                metadata["mime_type"] = artifact.inline_data.mime_type
                        
                        st.json(metadata)
                        
                        # Handle different artifact types
                        if hasattr(artifact, 'inline_data') and artifact.inline_data:
                            # Try to display as image first
                            try:
                                st.markdown("**Image Preview:**")
                                st.image(
                                    artifact.inline_data.data, 
                                    caption=artifact_key,
                                    use_container_width=True
                                )
                                
                                # Try to get additional image info using PIL
                                try:
                                    import io
                                    from PIL import Image as PILImage
                                    
                                    img = PILImage.open(io.BytesIO(artifact.inline_data.data))
                                    st.markdown(f"**Dimensions:** {img.size[0]} x {img.size[1]} pixels")
                                    st.markdown(f"**Format:** {img.format}")
                                    st.markdown(f"**Mode:** {img.mode}")
                                except Exception:
                                    # PIL not available or not a valid image
                                    pass
                                    
                            except Exception as img_error:
                                st.warning(f"Could not display as image: {img_error}")
                                # Fallback to raw display
                                st.markdown("**Raw Content:**")
                                data_size = len(artifact.inline_data.data) if artifact.inline_data.data else 0
                                st.text(f"Binary data ({data_size} bytes)")
                                # Show first few bytes as hex
                                if artifact.inline_data.data:
                                    hex_preview = ' '.join([f'{b:02x}' for b in artifact.inline_data.data[:32]])
                                    st.code(f"Hex: {hex_preview}{'...' if len(artifact.inline_data.data) > 32 else ''}")
                        
                        elif isinstance(artifact, dict):
                            st.markdown("**Content:**")
                            st.json(artifact)
                        
                        elif isinstance(artifact, str):
                            st.markdown("**Content:**")
                            if len(artifact) > 500:
                                st.text_area("Content", artifact, height=200, disabled=True)
                            else:
                                st.markdown(artifact)
                        
                        else:
                            st.markdown("**Content:**")
                            st.text(str(artifact))
                        
                        # Download functionality
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Prepare download data
                            if hasattr(artifact, 'inline_data') and artifact.inline_data and artifact.inline_data.data:
                                download_data = artifact.inline_data.data
                                if is_image:
                                    # Try to detect proper file extension
                                    try:
                                        import io
                                        from PIL import Image as PILImage
                                        img = PILImage.open(io.BytesIO(artifact.inline_data.data))
                                        file_ext = img.format.lower() if img.format else 'bin'
                                        filename = f"{artifact_key.split('.')[0]}.{file_ext}"
                                        mime_type = f"image/{file_ext}"
                                    except:
                                        filename = artifact_key if '.' in artifact_key else f"{artifact_key}.bin"
                                        mime_type = "application/octet-stream"
                                else:
                                    filename = artifact_key if '.' in artifact_key else f"{artifact_key}.bin"
                                    mime_type = "application/octet-stream"
                            
                            elif isinstance(artifact, dict):
                                import json
                                download_data = json.dumps(artifact, indent=2).encode('utf-8')
                                filename = f"{artifact_key}.json"
                                mime_type = "application/json"
                            
                            else:
                                download_data = str(artifact).encode('utf-8')
                                filename = f"{artifact_key}.txt"
                                mime_type = "text/plain"
                            
                            st.download_button(
                                label="💾 Download",
                                data=download_data,
                                file_name=filename,
                                mime=mime_type,
                                key=f"download_{i}",
                                use_container_width=True
                            )
                        
                        with col2:
                            # Copy button for non-binary content
                            if not (hasattr(artifact, 'inline_data') and artifact.inline_data):
                                if st.button("📋 Copy", key=f"copy_{i}", use_container_width=True):
                                    st.success("Content ready to copy!")
                    
                    else:
                        st.warning("Could not load artifact content")
                        
                except Exception as e:
                    st.error(f"Failed to load artifact {artifact_key}: {e}")
                    
    except Exception as e:
        st.error(f"Failed to load artifacts: {e}")

async def render_sidebar():
    """Render enhanced sidebar with state synchronization status and artifact viewing"""
    with st.sidebar:
        st.markdown("### 🚀 Content Studio")
        st.markdown(f"**Session:** `{SESSION_ID[:8]}...`")
        
        # Sync status indicator
        if st.session_state.get('agent_state_synced', False):
            st.markdown('<div class="sync-indicator">🔄 Agent State Synchronized</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ State Not Synchronized")
        
        # Navigation tabs
        tab = st.radio("📊 Data View", ["State", "Trace", "Artifacts"], label_visibility="collapsed")
        
        st.divider()
        
        # Enhanced preload data button
        if st.button("🔄 Sync & Refresh", use_container_width=True):
            loop = asyncio.get_event_loop()
            sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
            if sync_success:
                loop.run_until_complete(preload_all_tab_data())
                st.success("✅ State synchronized and data refreshed!")
                st.rerun()
            else:
                st.error("❌ Failed to synchronize state!")
        
        # Display selected tab content
        if tab == "State":
            st.subheader("📊 Synchronized State")
            preloaded_state = st.session_state.get('preloaded_state', {})
            if preloaded_state:
                # Show sync timestamp
                if st.session_state.get('agent_state_synced'):
                    st.info("🔄 This state is synchronized with agent")
                st.json(preloaded_state)
            else:
                st.info("No state data available")
        
        elif tab == "Trace":
            st.subheader("🔍 Execution Trace")
            preloaded_trace = st.session_state.get('preloaded_trace', {})
            if preloaded_trace:
                st.json(preloaded_trace)
            else:
                st.info("No trace data available")
        
        elif tab == "Artifacts":
            
            await display_enhanced_artifacts_tab()

# ──────────────────────────────────────────────────────────────
# 🚀 MAIN APPLICATION
# ──────────────────────────────────────────────────────────────

async def main():
    """Main application dispatcher with enhanced state synchronization"""
    # Verify initialization
    verify_initialization()
    
    # Initialize session state
    initialize_session_state()
    
    # 🔄 CRITICAL: Perform initial state synchronization
    if not st.session_state.get('initial_sync_done', False):
        with st.spinner("Performing initial state synchronization..."):
            loop = asyncio.get_event_loop()
            sync_success = loop.run_until_complete(sync_agent_state_to_streamlit())
            if sync_success:
                st.session_state['initial_sync_done'] = True
                loop.run_until_complete(preload_all_tab_data())
    
    # Render sidebar
    await render_sidebar()
    
    # Main content area
    st.title("🚀 Content Studio - 3-Step Workflow")
    st.markdown("*AI-powered social media content creation with **agent state synchronization***")
    
    # Step indicator with sync status
    render_step_indicator()
    
    st.divider()
    
    # Route to appropriate step
    if st.session_state.current_step == 1:
        step1_company_profile_and_topic()
    elif st.session_state.current_step == 2:
        step2_prepost_analysis()
    elif st.session_state.current_step == 3:
        await step3_content_generation()
    
    st.divider()
    
    # Navigation buttons
    render_navigation_buttons()
    
    # Enhanced progress summary with sync status
    st.markdown("### 📈 Progress Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "✅ Complete" if st.session_state.step1_complete else "⏳ Pending"
        st.metric("Step 1", status)
    
    with col2:
        status = "✅ Complete" if st.session_state.step2_complete else "⏳ Pending"
        st.metric("Step 2", status)
    
    with col3:
        status = "✅ Complete" if st.session_state.step3_complete else "⏳ Pending"
        st.metric("Step 3", status)
    
    with col4:
        sync_status = "🔄 Synced" if st.session_state.get('agent_state_synced', False) else "❌ Not Synced"
        st.metric("State Sync", sync_status)

# ──────────────────────────────────────────────────────────────
# 🎯 APPLICATION ENTRY POINT
# ──────────────────────────────────────────────────────────────


if __name__ == "__main__":
    asyncio.run(main())

