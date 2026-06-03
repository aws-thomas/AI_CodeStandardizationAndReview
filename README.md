# myKB - Kanban Board Application

A lightweight, web-based Kanban board application for managing tasks and workflows.

## Project Overview

**myKB** is a modern Kanban board application with the following features:

- Create and manage multiple boards
- Add, rename, and reorder columns (e.g., To Do, In Progress, Done)
- Create, edit, move, and delete cards within columns
- Drag-and-drop cards between columns
- Persist board state across sessions

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database
- **SQLAlchemy** - ORM for database operations
- **Uvicorn** - ASGI server
- **uv** - Fast Python package manager

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React 18** - UI library

## Project Structure

```
myKB/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── database.py     # Database configuration
│   │   ├── models/         # Database models
│   │   └── routes/         # API routes
│   ├── pyproject.toml      # Python dependencies (uv)
│   └── .gitignore
│
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   └── globals.css    # Global styles
│   ├── components/        # React components
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   ├── tsconfig.json      # TypeScript config
│   ├── next.config.js     # Next.js config
│   ├── tailwind.config.js # Tailwind config
│   └── .gitignore
│
├── BOB.md                 # Project guidelines
└── README.md              # This file
```

## Getting Started

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **npm** - Node package manager (comes with Node.js)

**Optional:**
- **uv** - Fast Python package manager (alternative to pip)
  ```bash
  # Install uv (macOS/Linux)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # Install uv (Windows)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
   
   *Or if you have uv installed:*
   ```bash
   uv sync
   ```

3. Run the FastAPI development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   
   *Or with uv:*
   ```bash
   uv run uvicorn app.main:app --reload
   ```

4. The backend API will be available at:
   - **API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the Next.js development server:
   ```bash
   npm run dev
   ```

4. The frontend will be available at:
   - **App**: http://localhost:3000

### Running Both Services

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Development

### Backend Development

- **Add new routes**: Create files in `backend/app/routes/`
- **Add models**: Create files in `backend/app/models/`
- **Database**: SQLite database will be created as `backend/mykb.db`

### Frontend Development

- **Add components**: Create files in `frontend/components/`
- **Add pages**: Create files in `frontend/app/`
- **Styling**: Use Tailwind CSS utility classes

## Code Quality Standards

### Backend
- All database writes must be wrapped in a transaction
- Never return raw exception messages or stack traces to the client
- Use parameterized queries only — no string-formatted SQL
- Write descriptive comments on what functions do

### Frontend
- No `any` types in TypeScript — use explicit interfaces
- All API calls must handle loading and error states visibly
- Write descriptive comments on what functions do

### General
- Write simple code, do not overengineer
- Code readability must be prioritized
- Code must be readable to a junior developer
- Use camelCase for variables
- No commented-out code
- Never use emojis

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

## License

This project is for educational and personal use.

## Next Steps

1. Install dependencies for both backend and frontend
2. Start both development servers
3. Begin implementing Kanban board features
4. Add database models for boards, columns, and cards
5. Create API endpoints for CRUD operations
6. Build frontend components for board visualization
7. Implement drag-and-drop functionality

---

**Happy coding! 🚀**