# SupplyGuard AI (Frontend Context)

## 🚀 Project Overview
**SupplyGuard AI Frontend** is the user interface for the AI-powered supply chain risk intelligence system. It provides a dashboard for visualizing supply chain networks, monitoring real-time risks, running simulations, and interacting with an AI agent for insights.

**Core Goal:** Visualize predictive decision intelligence for supply chain management.

**Key Features:**
*   **Risk Dashboard:** Real-time metrics and alerts for supply chain disruptions.
*   **AI Chat Interface:** Conversational agent to query data and get recommendations.
*   **Supplier & Outlet Management:** Detailed views of inventory and risk status.
*   **Simulation:** Interface to trigger and view supply chain simulation results.

## 🛠️ Tech Stack

### Framework & Core
*   **Framework:** Next.js 16.1.0 (App Router)
*   **Language:** TypeScript
*   **Runtime:** React 19.2.3
*   **Build Tool:** Next.js Compiler

### Styling & UI
*   **Styling:** Tailwind CSS v4
*   **Components:** Radix UI (Primitives), Lucide React (Icons)
*   **Utilities:** `clsx`, `tailwind-merge`, `class-variance-authority`

### State & API
*   **State Management:** React Hooks (`useState`, `useEffect`)
*   **API Client:** Custom fetch wrapper in `lib/api.ts`
*   **Markdown Rendering:** `react-markdown` (for AI responses)

## 🏗️ Building and Running

### Prerequisites
*   Node.js (LTS recommended)
*   npm

### Setup Instructions
1.  **Install dependencies:**
    ```bash
    npm install
    ```
2.  **Environment Variables:**
    (Optional) Create a `.env.local` file to override defaults:
    ```env
    NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
    ```
3.  **Run Development Server:**
    ```bash
    npm run dev
    ```
    *App available at:* `http://localhost:3000`

### Build & Lint
*   **Build:** `npm run build`
*   **Lint:** `npm run lint`

## 📂 Key Directories

### `app/`
*   `(dashboard)/`: Main authenticated application area.
    *   `dashboard/`: Overview page.
    *   `risks/`, `suppliers/`, `outlets/`, `simulation/`: Domain-specific pages.
*   `(marketing)/`: Public landing page.
*   `globals.css`: Global styles and Tailwind imports.
*   `layout.tsx`: Root layout structure.

### `components/`
*   `chat/`: AI Chat interface components (`AgentChat`, `ChatInput`, `ChatMessages`).
*   `dashboard/`: Dashboard-specific widgets (`OverviewMetrics`, `RiskScoreCard`).
*   `ui/`: Reusable UI primitives (buttons, cards, dialogs) - shadcn/ui style.
*   `risks/`, `suppliers/`, `outlets/`: Domain-specific tables and views.

### `lib/`
*   `api.ts`: Centralized API client methods organized by domain (`overview`, `risks`, `agent`, etc.).
*   `types.ts`: TypeScript interfaces for data models.
*   `utils.ts`: Helper functions (mostly for class merging).

## 📝 Development Conventions

*   **Routing:** Uses Next.js App Router with Route Groups `(folder)` to organize layouts without affecting URL paths.
*   **Styling:** Tailwind CSS utility classes are preferred. `cn()` utility is used for conditional class merging.
*   **API Integration:** All API calls should go through `lib/api.ts`. Do not fetch directly in components if possible.
*   **Components:** "dumb" UI components in `components/ui`, feature-specific components in their respective folders.
*   **Icons:** Use `lucide-react` for all icons.

## 🔗 Backend Integration
The frontend expects a backend running at `http://localhost:8000/api` (default).
Key API endpoints used:
*   `/agent/`: AI Chat interaction.
*   `/risks/`, `/suppliers/`, `/outlets/`: Data fetching for tables and details.
*   `/simulation/run`: Triggering risk simulations.
