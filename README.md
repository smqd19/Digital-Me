# Qasim's AI Avatar - Digital Portfolio Chatbot

An intelligent AI-powered chatbot that serves as a digital avatar, answering questions about my professional experience, projects, and skills. Built to showcase expertise in Generative AI, LLMs, and modern web development.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple)

## Features

- **Agentic Architecture**: Custom tool-calling agent that decides when to search experience, projects, or skills
- **RAG System**: Vector-based retrieval using ChromaDB for accurate, contextual responses
- **Real-time Chat**: Fast responses with streaming support
- **Modern UI**: Sleek dark theme with animations using Framer Motion
- **Semantic Search**: Intelligent matching of recruiter questions to relevant experience

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **LLM**: OpenAI GPT-4o-mini with native function calling
- **Vector Store**: ChromaDB with OpenAI embeddings
- **Architecture**: Custom agentic RAG (no LangChain dependency)

### Frontend
- **Framework**: Next.js 16 (React)
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion
- **Components**: Custom UI components with glassmorphism effects

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/        # Agentic chat logic
│   │   ├── models/        # Pydantic schemas
│   │   ├── prompts/       # System prompts
│   │   ├── retrieval/     # RAG & vector store
│   │   ├── tools/         # Agent tools (search, match)
│   │   ├── config.py      # Settings management
│   │   └── main.py        # FastAPI application
│   ├── data/
│   │   └── knowledge_base.json
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   └── hooks/         # Custom hooks
│   └── package.json
│
└── README.md
```

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### Backend Setup

```bash
cd backend

# Create virtual environment (using uv)
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
uv pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Run development server
npm run dev
```

Visit `http://localhost:3000` to see the application.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send a message and get a response |
| `/chat/stream` | POST | Stream response tokens |
| `/health` | GET | Health check |
| `/reindex` | POST | Reindex the knowledge base |

## Environment Variables

### Backend
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: LLM model (default: gpt-4o-mini)
- `CORS_ORIGINS`: Allowed frontend origins

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Deployment

- **Frontend**: Deployed on Vercel
- **Backend**: Deployed on Fly.io

## Architecture Highlights

### Why No LangChain?

This project intentionally avoids LangChain to demonstrate:
1. Deep understanding of LLM fundamentals
2. Lightweight, maintainable code
3. Full control over the agent loop
4. Faster cold starts in serverless environments

### Agent Flow

```
User Query → Agent receives message
           → Decides which tool(s) to call
           → Executes tool (search experience/projects/skills)
           → Receives context from vector store
           → Generates personalized response
```

## Author

**Muhammad Qasim Sheikh**  
Senior AI Engineer | 7+ Years Experience

- GitHub: [@smqd19](https://github.com/smqd19)
- LinkedIn: [Qasim Dawood](https://linkedin.com/in/qasim-dawood-a2b594143)

## License

MIT License - Feel free to use this as inspiration for your own portfolio chatbot!
