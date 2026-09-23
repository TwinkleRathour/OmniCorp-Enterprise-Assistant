import streamlit as st
import traceback
from azure.identity import ClientSecretCredential
from azure.ai.projects import AIProjectClient

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="OmniCorp Assistant",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 OmniCorp Enterprise Assistant")
st.caption("AI-Powered Corporate Knowledge & Task Assistant | Microsoft Foundry + RAG")

# ----------------- FOUNDRY CLIENT SETUP -----------------
ENDPOINT = "https://corporateai.services.ai.azure.com/api/projects/CorporateAI"
MY_AGENT = "OmniCorp-Assistant"
MY_VERSION = "3"

@st.cache_resource
def get_openai_client():
    credential = ClientSecretCredential(
        tenant_id=st.secrets["AZURE_TENANT_ID"],
        client_id=st.secrets["AZURE_CLIENT_ID"],
        client_secret=st.secrets["AZURE_CLIENT_SECRET"],
    )
    project_client = AIProjectClient(
        endpoint=ENDPOINT,
        credential=credential,
    )
    return project_client.get_openai_client()

client = get_openai_client()

# ----------------- SESSION STATE -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------- SIDEBAR TEST SCENARIOS -----------------
st.sidebar.title("📌 Quick Test Scenarios")
st.sidebar.write("Click any sample query to test agent capabilities live:")

scenarios = {
    "ASK: Leaves (RAG)": "What is the company policy for paternity leave and annual leave?",
    "ASK: Travel Limit (RAG)": "Can I claim hotel expenses of ₹7,500 per night for an official trip to Mumbai, and what is my daily meal per-diem allowance?",
    "FIND: Remaining Leaves (Python)": "How many annual leave days do I have remaining in my account?",
    "ACT: Raise IT Ticket (Python)": "My Wi-Fi keeps dropping out on the corporate network. Please create an IT ticket for this issue.",
    "GUARDRAIL: Mars Policy": "What is OmniCorp's official policy for employees stationed on Mars?"
}

for label, query in scenarios.items():
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.current_prompt = query

if st.sidebar.button("🔄 Reset Conversation", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# ----------------- DISPLAY CHAT HISTORY -----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------- USER INPUT & RUN EXECUTION -----------------
user_input = st.chat_input("Ask a corporate policy or request an action...")

if hasattr(st.session_state, "current_prompt") and st.session_state.current_prompt:
    user_input = st.session_state.current_prompt
    st.session_state.current_prompt = None

if user_input:
    # 1. Render user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Call Foundry Agent via responses API
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🔍 *Consulting enterprise knowledge base & tools...*")

        try:
            # Build conversation payload for the agent
            conversation_input = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            response = client.responses.create(
                input=conversation_input,
                extra_body={
                    "agent_reference": {
                        "name": MY_AGENT,
                        "version": MY_VERSION,
                        "type": "agent_reference"
                    }
                },
            )

            # Retrieve text response
            reply_text = getattr(response, "output_text", None) or str(response)

            placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

        except Exception as err:
            # Print the FULL traceback + underlying Azure error details to stdout
            # so it shows up in `az webapp log tail`. Streamlit only shows the
            # short repr of the exception in the UI, which hides the actual
            # resource/permission causing the 403.
            print("=" * 60, flush=True)
            print("AGENT CALL FAILED", flush=True)
            print(traceback.format_exc(), flush=True)

            # OpenAI SDK errors (openai.PermissionDeniedError etc.) expose the
            # parsed JSON body on `.body`, and the raw httpx response on
            # `.response`. Note: httpx's `.text` is a PROPERTY, not a method —
            # calling it as `.text()` raises TypeError and gets swallowed.
            print("--- err.body (parsed) ---", flush=True)
            try:
                print(getattr(err, "body", None), flush=True)
            except Exception as e:
                print(f"(could not read err.body: {e})", flush=True)

            print("--- err.message ---", flush=True)
            try:
                print(getattr(err, "message", None), flush=True)
            except Exception as e:
                print(f"(could not read err.message: {e})", flush=True)

            response_obj = getattr(err, "response", None)
            if response_obj is not None:
                print("--- response.status_code ---", flush=True)
                try:
                    print(response_obj.status_code, flush=True)
                except Exception as e:
                    print(f"(could not read status_code: {e})", flush=True)

                print("--- response.text (property, not called) ---", flush=True)
                try:
                    print(response_obj.text, flush=True)
                except Exception as e:
                    print(f"(could not read response.text: {e})", flush=True)

                print("--- response.headers ---", flush=True)
                try:
                    print(dict(response_obj.headers), flush=True)
                except Exception as e:
                    print(f"(could not read headers: {e})", flush=True)
            print("=" * 60, flush=True)

            placeholder.markdown(f"⚠️ **Error running agent:** `{err}`")
