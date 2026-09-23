import streamlit as st
import traceback
from openai import OpenAI

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

# The OpenAI-compatible surface of a Foundry project lives at {endpoint}/openai/v1
BASE_URL = ENDPOINT.rstrip("/") + "/openai/v1"


@st.cache_resource
def get_openai_client():
    """
    Authenticate with the Foundry PROJECT API KEY instead of an Entra ID token.

    The Entra ID path (managed identity / service principal) was returning an
    empty-body 403 from the istio gateway. The project API key is a completely
    separate auth path and does not depend on RBAC role assignments at all.

    The key comes from: Foundry portal -> Manage -> Project details -> API Key
    """
    api_key = st.secrets["AZURE_AI_API_KEY"]
    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL,
    )


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

            reply_text = getattr(response, "output_text", None) or str(response)

            placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})

        except Exception as err:
            print("=" * 60, flush=True)
            print("AGENT CALL FAILED", flush=True)
            print(traceback.format_exc(), flush=True)

            print("--- err.body ---", flush=True)
            try:
                print(getattr(err, "body", None), flush=True)
            except Exception as e:
                print(f"(could not read err.body: {e})", flush=True)

            response_obj = getattr(err, "response", None)
            if response_obj is not None:
                try:
                    print("--- response.status_code ---", flush=True)
                    print(response_obj.status_code, flush=True)
                    print("--- response.text ---", flush=True)
                    print(response_obj.text, flush=True)
                    print("--- response.headers ---", flush=True)
                    print(dict(response_obj.headers), flush=True)
                except Exception as e:
                    print(f"(could not read response details: {e})", flush=True)
            print("=" * 60, flush=True)

            placeholder.markdown(f"⚠️ **Error running agent:** `{err}`")
