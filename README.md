# 🏢 OmniCorp Enterprise Assistant

An AI-powered enterprise assistant that combines **Retrieval-Augmented Generation (RAG)**, **Microsoft Foundry**, and **Python-based enterprise tools** to provide employees with intelligent answers and perform common workplace tasks.

The application provides a conversational interface where employees can ask questions about company policies, retrieve personal information, and perform actions such as raising IT tickets and submitting expense claims.

---

## ✨ Features

### 🧠 Enterprise Knowledge Q&A

Uses **RAG (Retrieval-Augmented Generation)** to answer questions from enterprise knowledge documents, including:

- HR Leave & Benefits Policy
- IT Support & Hardware SOP
- Travel & Expense Policy

Users can ask questions in natural language instead of manually searching through company documents.

### 🤖 Microsoft Foundry Agent

The application integrates with a **Microsoft Foundry Agent** to:

- Understand user requests
- Retrieve relevant enterprise information
- Select appropriate tools
- Generate contextual responses
- Handle questions outside the available knowledge base

### 👤 Employee Information

The assistant can retrieve employee-specific information such as:

- Remaining annual leave
- Sick leave balance
- Paternity leave entitlement
- Assigned device
- Device asset information

### 🎫 IT Ticket Creation

Employees can describe an IT problem in natural language, and the assistant can create an IT incident containing:

- Issue category
- Priority
- Timestamp
- SLA information
- Incident details

### 💰 Expense Claims

The assistant supports submitting expense claim information for downstream approval and auditing workflows.

### 💬 Conversational Interface

The application uses **Streamlit** to provide an interactive chat interface with conversation history.

---

# 🧠 System Architecture

```text
                    ┌─────────────────────────┐
                    │       User              │
                    │   Natural Language      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Streamlit UI       │
                    │        app.py           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Microsoft Foundry     │
                    │        Agent            │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
                 ▼                                ▼
       ┌────────────────────┐          ┌────────────────────┐
       │    RAG Knowledge   │          │  Corporate Tools   │
       │       Base         │          │                    │
       ├────────────────────┤          ├────────────────────┤
       │ HR Policy          │          │ Leave Balance      │
       │ IT SOP             │          │ Device Information │
       │ Travel Policy      │          │ IT Ticket          │
       └────────────────────┘          │ Expense Claim      │
                                       └────────────────────┘
