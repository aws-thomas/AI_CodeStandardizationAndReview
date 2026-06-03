
You will create a web app called myKB. It is a web-based Kanban board application. The core features include creating and managing multiple boards, adding, renaming, and reordering columns, creating, editing, moving, and deleting cards within columns, and drag-and-drop functionality to move cards between columns. The application should persist board state across sessions. The planned stack includes Next.js with TypeScript for the frontend, FastAPI (Python) for the backend, SQLite for the database, and Tailwind CSS for styling.


## Project Overview: myKB

**myKB** is a lightweight, web-based Kanban board application. Core features:

- Create and manage multiple boards
- Add, rename, and reorder columns (e.g. To Do, In Progress, Done)
- Create, edit, move, and delete cards within columns
- Drag-and-drop cards between columns
- Persist board state across sessions

**Planned stack:**
- Frontend: Next.js with TypeScript
- Backend: FastAPI (Python)
- Database: SQLite
- Styling: Tailwind CSS


# myKB — IBM Bob Instructions

## Project
Web-based Kanban board. Backend: FastAPI + SQLite. Frontend: Next.js TypeScript.

## Code Quality Standards
- Backend: all database writes must be wrapped in a transaction; 
- Backend: never return raw exception messages or stack traces to the client
- Backend: use parameterized queries only — no string-formatted SQL
- Frontend: no `any` types in TypeScript — use explicit interfaces
- Frontend: all API calls must handle loading and error states visibly
- Write descriptive comments on what functions do
- Write simple code, do not overengineer, but code readability must be prioritized, code must be readable to a junior developer.
- When writing variables use camel casing.
- No commented-out code 
- Do not use emojis, and do not write # Made with Bob comments in the code. 
