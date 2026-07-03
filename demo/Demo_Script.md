# CreditGuard AI — Professional Demo Script

This script outlines the flow, voiceover directions, and screen views for a 3-5 minute stakeholder presentation.

---

## Part 1: Landing Page & Portal Core (Duration: 0:00 - 0:45)
- **Visuals**: Start on the Home landing page (`/`). Scroll smoothly past the Hero title and the rotating 3D Credit Card. Highlight the stats cards showing 98.7% accuracy and the features grid.
- **Actions**: Click the theme toggle switch in the bottom-left sidebar to show light mode, then toggle back to dark mode. Click the "Portal Home" nav link.

---

## Part 2: Authentication & Registration (Duration: 0:45 - 1:15)
- **Visuals**: Click the "Sign In" or "Get Started" buttons. Show the premium glassmorphic registration layout (`/auth/register`).
- **Actions**: Complete registration fields for a demo user, submit, then sign in with the user credentials (`/auth/login`). Show session management redirection to the Dashboard.

---

## Part 3: New Credit Application Wizard (Duration: 1:15 - 2:00)
- **Visuals**: Navigate to "New Application" (`/predict`). Review the multi-step progress indicators.
- **Actions**:
  - **Step 1**: Enter demographic features (Gender: Female, Age: 34, Marital Status: Married, 2 children, Higher Education, Housing: Municipal). Click Next.
  - **Step 2**: Enter financial features (Income Source: Commercial Associate, Income: $85,000, 6 years employed, monthly debt: $250, requested limit: $10,000, credit Bureau: Good). Click Next.
  - **Step 3**: Review the dynamic confirmation grid. Click Next.
  - **Step 4**: Trigger "Submit Application" to execute pipeline inference.

---

## Part 4: Explainable AI Result Assessment (Duration: 2:00 - 2:45)
- **Visuals**: Result outcome screen (`/predict` outcome). Show the animated probability gauge meter filling up. Highlight the approved status badge, risk profiles, and LIME local feature contribution cards.
- **Actions**: Explain positive contributing factors (e.g. good credit bureau, low DTI) and negative risk factors. Explain the natural language recommendations.

---

## Part 5: History Logs & Analytics (Duration: 2:45 - 3:30)
- **Visuals**: Navigate to "Prediction History" (`/history`). Show filter chips, search input queries, pagination buttons.
- **Actions**: Filter by "Approved Only", search for specific IDs. Click the Export CSV button.
- **Visuals**: Navigate to "Dashboard" (`/admin`). Scroll through the Chart.js doughnut, bar, and timeline charts. Toggle between the daily and monthly line chart views.

---

## Part 6: PDF Export & Logout (Duration: 3:30 - 4:00)
- **Visuals**: From the history or result view, click "View Printable Report" (`/report/<app_id>`). Review the clean layout, QR code validation box, and officer signature block.
- **Actions**: Trigger print dialog (`Ctrl + P`), close it, then click "Log Out" in the sidebar to return to the landing home page.
