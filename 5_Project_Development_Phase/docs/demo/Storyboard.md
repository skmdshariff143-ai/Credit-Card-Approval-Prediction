# CreditGuard AI — Demonstration Video Storyboard

This storyboard outlines the visual sequence, screen focus areas, and content milestones for the 3-to-5 minute product demonstration video.

---

## 🎬 Storyboard Timeline

### Scene 1: Introduction (0:00 - 0:25)
* **Visual**: Show the `Intro.png` slide (CreditGuard AI: Next-Gen Credit Decisioning). Smooth fade transition into the browser showing the landing page with floating blob background animations.
* **On-Screen Focus**: Hero header, premium dark glassmorphic navigation bar, and primary "Launch Application" CTA.
* **Objective**: Establish branding and define the project's scope.

### Scene 2: Problem Statement & Tech Stack (0:25 - 0:55)
* **Visual**: Scroll down the landing page to reveal the "Technology Stack" section.
* **On-Screen Focus**: Hover effects on tech cards (Flask, Scikit-learn, XGBoost, SQLite, Chart.js, Docker, Vercel).
* **Objective**: Explain the banker's core problem (delinquency defaults and lost revenue due to Type I/II errors) and the automated, ML-driven solution.

### Scene 3: User Authentication (0:55 - 1:15)
* **Visual**: Click "Sign In" in the navigation bar to navigate to `/auth/login`. Enter credentials and click "Submit".
* **On-Screen Focus**: Beautiful glassmorphic card layout, clean validation messaging, and smooth redirect to user dashboard page.
* **Objective**: Demonstrate secure multi-user session management via Flask-Login.

### Scene 4: Predictive Analytics Dashboard (1:15 - 1:45)
* **Visual**: Navigate through the analytics dashboard on the User Portal.
* **On-Screen Focus**: Chart.js charts (doughnut charts showing approval splits, daily line graphs showing volume trends) and live statistics cards.
* **Objective**: Show how bankers and users review aggregated decision metrics in real-time.

### Scene 5: Conversational Prediction Wizard (1:45 - 2:30)
* **Visual**: Click "New Prediction" in the sidebar to navigate to the 4-Step wizard form (`/predict`). Fill out sample data step-by-step.
* **On-Screen Focus**: Slide transitions, progress bar updating dynamically, active option outlines, and the final review step showing input values.
* **Objective**: Highlight the mobile-responsive, frictionless, conversational UI/UX design.

### Scene 6: Explainable AI & Scorecard (2:30 - 3:15)
* **Visual**: Submit the wizard form and load the results page (`/result/<app_id>`).
* **On-Screen Focus**: The animated score gauge (probability of approval), LIME explainability metrics (horizontal bars showing risk and support feature impacts), and actionable recommendations.
* **Objective**: Demonstrate that the AI is fully transparent and compliant with bank decision auditing guidelines.

### Scene 7: Prediction History & Printable Reports (3:15 - 3:55)
* **Visual**: Navigate to "Prediction History" in the sidebar, search for the application ID, and click "Print Report".
* **On-Screen Focus**: Writable SQLite logs table, search filter queries, and the print-ready report page showing the verification QR code.
* **Objective**: Show ledger auditing, history management, and reporting with instant verification.

### Scene 8: Codebase & Git Pipeline (3:55 - 4:25)
* **Visual**: Quick walkthrough of the GitHub repository.
* **On-Screen Focus**: Modular folder structures (`app/`, `config/`, `models/`, `src/`, `tests/`), CI/CD pytest status, and deployment tags.
* **Objective**: Highlight development standards, code coverage, and automated linting.

### Scene 9: Conclusion & Outro (4:25 - 4:45)
* **Visual**: Show `Outro.png` slide with thank you credits, live links, and GitHub tags.
* **Objective**: Close with clear call-to-actions.
