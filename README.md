# Phantom Directive Chat

An AI-powered chat interface that allows users to query declassified CIA documents using RAG (Retrieval-Augmented Generation) technology. The application combines the power of Claude 3 Sonnet with vector search capabilities to provide accurate, sourced responses from official CIA documents.

## 🌐 Live Demo
Visit the live application: [phantomdirective.streamlit.app](https://phantomdirective.streamlit.app)

## 🚀 Features
- Real-time chat interface with AI responses
- Source citations from declassified CIA documents
- Vector-based semantic search using Pinecone
- Detailed source viewing with expandable sections
- Styled with a hacker-inspired black and neon green theme

## 🛠️ Technology Stack
- **Frontend**: Streamlit
- **AI Models**: 
  - Claude 3 Sonnet (Anthropic) for response generation
  - OpenAI text-embedding-3-small for vector embeddings
- **Vector Database**: Pinecone
- **Language**: Python 3.9+

## 🔧 Local Development
1. Clone the repository
git clone https://github.com/MersivMedia/phantom-directive-chat.git

2. Install dependencies
pip install -r requirements.txt

3. Create a `.env` file with the following variables:
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=aws
PINECONE_INDEX_NAME=phantomdirective
OPENAI_API_KEY=your_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

4. Run the application
streamlit run app.py

## 📚 Project Structure
- `app.py`: Main application file with chat interface
- `requirements.txt`: Project dependencies

## 🔐 Security Note
This application uses publicly available declassified documents from the CIA website. It is designed for research and entertainment purposes only.

## 🤝 Contributing
Feel free to open issues or submit pull requests for improvements.

## 📝 License
[MIT License](LICENSE)
