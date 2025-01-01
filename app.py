import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
from anthropic import Anthropic
from typing import List, Dict, Any
import streamlit as st
from operator import attrgetter

# Load environment variables
load_dotenv()

# Custom CSS
st.markdown("""
<style>
    /* Dark theme with neon green accents */
    .stApp {
        background-color: #0a0a0a !important;
    }
    
    /* Chat input placeholder color */
    .stChatInput textarea::placeholder {
        color: #00ff00 !important;
        opacity: 0.7;
    }
    
    /* All text elements */
    .stApp, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stChatMessage {
        color: #00ff00 !important;
    }
    
    /* Chat messages and input */
    .stChatMessage, .stChatInput {
        background-color: #1a1a1a !important;
        border: 1px solid #00ff00 !important;
        width: 650px !important;  /* Set fixed width for both */
        margin: 0 auto !important;
        padding-right: 20px !important;  /* Add more padding on right side */
    }
    
    /* Chat input styling */
    section[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 100px !important;
        left: 0 !important;
        right: 0 !important;
        background-color: #0a0a0a !important;
        padding: 0 !important;
        z-index: 999 !important;
    }
    
    /* Control text input width */
    .stChatInput > div {
        width: 650px !important;  /* Match chat message width */
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    /* Ensure the text input itself is properly contained */
    .stChatInput textarea {
        width: 100% !important;
        box-sizing: border-box !important;
        color: #00ff00 !important;
        background-color: #1a1a1a !important;
        border: 1px solid #00ff00 !important;
        padding: 8px 12px !important;
    }
    
    /* Container for the input background */
    div[data-testid="stChatInputContainer"] {
        width: 650px !important;  /* Match chat message width */
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    /* Style placeholder text */
    .stChatInput textarea::placeholder {
        color: #00ff00 !important;
        opacity: 0.7 !important;
    }
    
    /* Remove white background from chat container */
    .stChatContainer, div[data-testid="stChatMessageInput"] {
        background-color: #0a0a0a !important;
    }
    
    /* Buttons and interactive elements */
    .stButton>button {
        background-color: #1a1a1a !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background-color: #1a1a1a !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    
    /* Headers */
    h1, h2, h3, [data-testid="stHeader"] {
        color: #00ff00 !important;
    }
    
    /* Center main title only */
    .stApp > header + div [data-testid="stMarkdownContainer"] > div:first-child > h1 {
        text-align: center !important;
        width: 100% !important;
        margin: 20px 0 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #00ff00 !important;
    }
    
    /* Help icon */
    .help-icon {
        position: fixed;
        top: 20px;
        right: 20px;
        cursor: pointer;
        color: #00ff00;
        font-size: 24px;
        z-index: 1000;
    }
    
    /* Disclaimer modal */
    .disclaimer-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.8);
        z-index: 999;
    }
    
    .disclaimer-content {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #1a1a1a;
        padding: 2rem;
        border: 2px solid #00ff00;
        border-radius: 10px;
        z-index: 1000;
        max-width: 600px;
        text-align: center;
        color: #00ff00;
    }
    
    /* Sticky Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0a0a0a;
        color: #00ff00;
        text-align: center;
        padding: 10px 0;
        border-top: 1px solid #00ff00;
        z-index: 998;
    }
    
    .footer a {
        color: #00ff00;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 5px;
    }
    
    .social-icons svg {
        width: 24px;
        height: 24px;
        fill: #00ff00;
        transition: fill 0.3s ease;
    }
    
    .social-icons a:hover svg {
        fill: #66ff66;
    }
    
    /* Add padding to main content to prevent footer overlap */
    .main-content {
        padding-bottom: 50px !important;
    }
    
    /* Adjust chat input position */
    section[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 100px !important;  /* Increased distance from bottom */
        left: 0 !important;
        right: 0 !important;
        background-color: #0a0a0a !important;
        padding: 20px !important;
        z-index: 999 !important;
    }
    
    /* Force black background on all chat-related elements */
    .st-emotion-cache-128upt6,
    .st-emotion-cache-12cetgn,
    .st-emotion-cache-0,
    .st-emotion-cache-b95f0i,
    .st-emotion-cache-1n76uvr,
    .st-emotion-cache-ke1f9q,
    .st-emotion-cache-1wpj71q,
    .st-emotion-cache-s1k4sy,
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    .stVerticalBlock,
    .stElementContainer {
        background-color: #0a0a0a !important;
    }

    section[data-testid="stChatInput"] > div {
        background-color: #0a0a0a !important;
    }
    
    div[data-testid="stChatMessageInput"] > div {
        background-color: #0a0a0a !important;
    }
    
    /* Adjust main chat container to not overlap with fixed input */
    .stChatContainer {
        margin-bottom: 100px !important;
        background-color: #0a0a0a !important;
        overflow-y: auto !important;
        height: auto !important;
        min-height: 100vh !important;
        padding: 0 20px !important;
    }
    
    /* Ensure all backgrounds are black */
    .stMarkdown, .stChatMessage, div[class*="stChatInput"] {
        background-color: #0a0a0a !important;
    }

    /* Additional container styling */
    div[data-testid="stBottomBlockContainer"] {
        position: fixed !important;
        bottom: 120px !important;
        z-index: 998 !important;
        width: 100% !important;
    }

    /* Ensure content is scrollable */
    .main .block-container {
        padding-bottom: 300px !important;
        overflow-y: auto !important;
        height: auto !important;
    }

    /* Style scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background-color: #0a0a0a;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #00ff00;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-track {
        background-color: #1a1a1a;
    }

    /* Ensure expandable sections are fully visible */
    .streamlit-expanderContent {
        background-color: #0a0a0a !important;
        margin-bottom: 10px !important;
    }

    /* Main app container */
    .stApp {
        height: 100vh !important;
        overflow-y: auto !important;
        padding: 0 20px !important;
    }

    /* Chat message container */
    .stChatMessage {
        margin-bottom: 20px !important;
    }

    /* Message content */
    .stMarkdown {
        overflow: visible !important;
    }

    /* Extra padding for sources section */
    div[data-testid="stExpander"] {
        margin-bottom: 15px !important;
    }

    /* Additional padding for the last few sources */
    div[data-testid="stExpanderDetails"]:last-child,
    .stChatMessage:last-child {
        margin-bottom: 40px !important;  /* Extra space for last sources */
    }

    /* Sources section container */
    .stChatMessage div:has(> div[data-testid="stExpander"]) {
        padding-bottom: 350px !important;
    }

    /* Remove external padding from chat containers */
    div.stChatFloating {
        padding: 0 !important;
    }

    /* Remove padding from bottom block container and its children */
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    .st-emotion-cache-b95f0i,
    .stVerticalBlock,
    .stElementContainer,
    .st-emotion-cache-ke1f9q,
    .st-emotion-cache-1wpj71q,
    .st-emotion-cache-s1k4sy {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Ensure input container matches exact width */
    div[data-testid="stBottomBlockContainer"] {
        width: 650px !important;
        margin: 0 auto !important;
    }

    /* Remove any flex spacing */
    .stVerticalBlock {
        gap: 0 !important;
    }

    /* Ensure chat message container aligns with input */
    .stChatMessage {
        margin-left: auto !important;
        margin-right: auto !important;
        box-sizing: border-box !important;
    }
</style>

<div class="help-icon" onclick="showDisclaimer()">❔</div>

<div id="disclaimerModal" class="disclaimer-modal">
    <div class="disclaimer-content">
        <h2 style="color: #00ff00;">Welcome to Phantom Directive</h2>
        <p>This is an AI-powered RAG (Retrieval-Augmented Generation) chat application that utilizes declassified CIA documents from their public website.</p>
        <p>The application is designed for research and entertainment purposes only.</p>
        <p><strong>Disclaimer:</strong> We are not responsible for any misuse of this tool. All information provided comes from publicly available documents.</p>
        <button onclick="hideDisclaimer()" 
                style="
                    background-color: #1a1a1a;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    padding: 0.5rem 1rem;
                    margin-top: 1rem;
                    cursor: pointer;
                ">
            I Understand
        </button>
    </div>
</div>

<script>
    function showDisclaimer() {
        document.getElementById('disclaimerModal').style.display = 'block';
    }
    
    function hideDisclaimer() {
        document.getElementById('disclaimerModal').style.display = 'none';
    }
    
    // Show disclaimer on first load
    if (!window.localStorage.getItem('disclaimerAccepted')) {
        showDisclaimer();
    }
    
    // Handle disclaimer acceptance
    document.querySelector('.disclaimer-content button').addEventListener('click', function() {
        window.localStorage.setItem('disclaimerAccepted', 'true');
        hideDisclaimer();
    });
</script>

<div class="footer">
    <div class="social-icons">
        <a href="https://x.com/PhantomDirectiv" target="_blank">
            <svg viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
        </a>
        <a href="https://github.com/mersivmedia" target="_blank">
            <svg viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
        </a>
        <a href="https://open.spotify.com/playlist/4OI20qKIocsrDEIWecG4cp" target="_blank">
            <svg viewBox="0 0 24 24">
                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
        </a>
    </div>
    <a href="https://mersivmedia.com" target="_blank">Made by Mersiv Media</a>
</div>
""", unsafe_allow_html=True)

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

# Get Pinecone index
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def create_embedding(text: str) -> List[float]:
    """Create embedding using OpenAI's text-embedding-3-small."""
    response = openai_client.embeddings.create(
        input=text,
        model=os.getenv("OPENAI_EMBEDDING_MODEL")
    )
    return response.data[0].embedding

def get_ai_response(query: str, results: list) -> str:
    """Generate a comprehensive response using Claude."""
    if not results:
        return "I couldn't find any relevant information in the documents."
    
    # Prepare context from results
    context_parts = []
    for i, result in enumerate(results, 1):
        if hasattr(result, 'metadata') and result.metadata:
            source = f"Source {i}: {result.metadata.get('file_name', 'Unknown')}, {result.metadata.get('source', 'Unknown')}"
            text = result.metadata.get('text', '')
            summary = result.metadata.get('summary', '')
            context_parts.append(f"{source}\nText: {text}\nSummary: {summary}\n")
    
    context = "\n\n".join(context_parts)
    
    # Generate response using Claude
    prompt = f"""Based on the following sources, please provide a comprehensive answer to this question: "{query}"

Context:
{context}

Please synthesize the information and provide a clear, well-structured response. Include relevant citations in parentheses, referencing the source number and location (e.g., Source 1, Page 5, Section 2).

Response:"""

    response = anthropic_client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL"),
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response.content[0].text

def search_all_namespaces(query: str, top_k: int = 5):
    """Search for similar vectors across all namespaces"""
    try:
        # Get query embedding
        query_embedding = create_embedding(query)
        
        # Get all namespaces
        stats = index.describe_index_stats()
        namespaces = list(stats.namespaces.keys())
        
        all_results = []
        
        # Search in each namespace
        for namespace in namespaces:
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
            
            # Add namespace information to each result
            for match in results.matches:
                match.namespace = namespace
            
            all_results.extend(results.matches)
        
        # Sort all results by score and take top_k
        all_results.sort(key=attrgetter('score'), reverse=True)
        return all_results[:top_k]
    
    except Exception as e:
        st.error(f"Error searching vectors: {str(e)}")
        return []

def show_disclaimer():
    # The disclaimer is now handled by the JavaScript in the CSS section
    pass

def main():
    st.title("Phantom Directive Chat V1")
    
    # Show disclaimer
    show_disclaimer()
    
    # Set fixed number of results
    top_k = 10
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "results" in message:
                st.write("---")
                st.write("Sources:")
                for i, result in enumerate(message["results"], 1):
                    with st.expander(f"Source {i}"):
                        if hasattr(result, 'metadata') and result.metadata:
                            st.write(f"**File:** {result.metadata.get('file_name', 'Unknown')}")
                            st.write(f"**Location:** {result.metadata.get('source', 'Unknown')}")
                            st.write("**Summary:**")
                            st.write(result.metadata.get('summary', 'No summary available'))
                            st.write("**Full Text:**")
                            st.write(result.metadata.get('text', 'No text available'))
    
    # Chat input
    if prompt := st.chat_input("Ask questions about the CIA..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                results = search_all_namespaces(prompt, top_k)
            
            if results:
                with st.spinner("Generating response..."):
                    response = get_ai_response(prompt, results)
                st.write(response)
                
                st.write("\n---\nDetailed Sources:")
                # Display results
                for i, result in enumerate(results, 1):
                    with st.expander(f"Source {i}"):
                        if hasattr(result, 'metadata') and result.metadata:
                            st.write(f"**File:** {result.metadata.get('file_name', 'Unknown')}")
                            st.write(f"**Location:** {result.metadata.get('source', 'Unknown')}")
                            st.write("**Summary:**")
                            st.write(result.metadata.get('summary', 'No summary available'))
                            st.write("**Full Text:**")
                            st.write(result.metadata.get('text', 'No text available'))
            else:
                response = "I couldn't find any relevant information in the documents."
                st.write(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "results": results
            })

if __name__ == "__main__":
    main() 