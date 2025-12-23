# SupplyGuard AI Frontend

## 🌐 Overview

The SupplyGuard AI frontend is a Next.js application that provides the user interface for the AI-driven supply chain disruption prediction system. It visualizes supply chain risks, predictions, and mitigation recommendations in an intuitive dashboard.

## 🛠️ Tech Stack

- **Framework**: Next.js 16.1.0
- **Language**: TypeScript
- **Runtime**: React 19.2.3
- **Styling**: Tailwind CSS
- **Build Tool**: Next.js compiler

## 📁 Project Structure

```
frontend/
├── README.md              # This file
├── package.json           # Dependencies and scripts
├── next.config.ts         # Next.js configuration
├── tsconfig.json          # TypeScript configuration
├── eslint.config.mjs      # ESLint configuration
├── postcss.config.mjs     # PostCSS configuration
├── app/                   # Application pages and routes
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── ...
├── components/            # Reusable UI components
├── lib/                   # Utility functions
├── public/                # Static assets
└── node_modules/          # Dependencies (gitignored)
```

## 🚀 Getting Started

### Prerequisites

Before setting up the project, ensure you have the following installed:
- Node.js (LTS recommended)
- npm or yarn package manager
- Git for version control

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm run dev
   ```
   
   Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### Building for Production

```bash
npm run build
```

### Starting Production Server

```bash
npm run start
```

### Linting

```bash
npm run lint
```

## 🏗️ Key Features

### Dashboard Components
- Supply chain risk visualization
- Prediction timeline and alerts
- Mitigation recommendation cards
- Interactive map of supply chain network
- Real-time risk scoring indicators

### Data Visualization
- Charts and graphs showing risk trends
- Geographic representation of disruptions
- Timeline of predicted events
- Impact assessment visualizations

## 🧪 Testing

Testing framework and instructions will be added during development:
```bash
# Run tests (TBD)
# npm run test
```

## 📊 API Integration

The frontend communicates with the backend API for:
- Supply chain disruption predictions
- Risk scoring calculations
- Mitigation recommendations
- Historical data analysis
- Real-time monitoring updates

## 🔧 Environment Variables

Configuration options (to be implemented):
- `NEXT_PUBLIC_API_URL`: Backend API endpoint
- `NEXT_PUBLIC_APP_ENV`: Application environment
- `NEXT_PUBLIC_MAPBOX_TOKEN`: Map visualization token (if needed)

## 🎨 Design System

The application follows a consistent design system with:
- Responsive layouts using Tailwind CSS
- Accessible color palette with sufficient contrast
- Consistent typography hierarchy
- Intuitive navigation patterns
- Data visualization best practices

## 📱 Responsive Design

The frontend is designed to be fully responsive:
- Mobile-first approach
- Tablet and desktop optimized layouts
- Touch-friendly interfaces
- Adaptive data visualization

## 🚢 Deployment

The application is ready for deployment to platforms like:
- Vercel (recommended for Next.js)
- Netlify
- AWS Amplify
- Custom hosting solutions

## 🤝 Contributing

During the hackathon:
1. Create feature branches for your work
2. Follow the established code style (ESLint + TypeScript)
3. Commit regularly with descriptive messages
4. Coordinate with team members on feature integration
5. Test components across different screen sizes

## 📄 License

[License information to be determined by the team]

---

Part of the SupplyGuard AI project for One AI Hackathon 2025