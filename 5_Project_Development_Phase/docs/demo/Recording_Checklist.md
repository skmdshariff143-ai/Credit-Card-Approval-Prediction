# Screen Recording Checklist — CreditGuard AI

Follow this step-by-step checklist to record a high-quality, professional video walk-through of the CreditGuard AI application.

---

## 🛠️ Recording Setup

1. **Resolution**: Enforce `1920×1080` (1080p Full HD) screen resolution.
2. **Browser**: Use Chrome or Firefox. Clear browsing history, zoom to 100%, and toggle on "Do Not Disturb" on your OS.
3. **Cursor Settings**: Enable a cursor highlight effect (e.g. yellow highlight circle around pointer) and mouse click animations.
4. **Recording Tool**: Use OBS Studio, Camtasia, or Loom with 60 FPS settings.
5. **Server Status**: Ensure the Vercel deployment is active: [credit-card-approval-prediction-lac.vercel.app](https://credit-card-approval-prediction-lac.vercel.app).

---

## 📹 Recording Steps & Timeline Checklist

### Step 1: Landing Page & Hero Section (0:00 - 0:25)
- [ ] Load the main landing page.
- [ ] Wait 3 seconds for the initial animations (fade-in, glowing blobs) to settle.
- [ ] Slowly hover your mouse over the navigation links ("Home", "Sign In", "Register").
- [ ] Scroll down slowly to show the introduction text card.

### Step 2: Technology Stack Showcase (0:25 - 0:55)
- [ ] Continue scrolling down to the "Technology Stack" section.
- [ ] Pause for 2 seconds.
- [ ] Slowly hover over the individual tech badges (Flask, Scikit-learn, XGBoost, etc.) to trigger the zoom and lift hover animations.
- [ ] Scroll back to the top.

### Step 3: Login Portal (0:55 - 1:15)
- [ ] Click the "Sign In" button in the navigation bar.
- [ ] Enter the test credentials:
  - Username: `admin` (or register a new user)
  - Password: `admin_password`
- [ ] Hover over the "Sign In" submit button to show the hover effect, then click.
- [ ] Wait for the dashboard page to load.

### Step 4: Analytics Dashboard (1:15 - 1:45)
- [ ] Let the dashboard page load fully and wait for the Chart.js animation to complete.
- [ ] Slowly hover over the statistical metric cards (Total Predictions, Approval Rate).
- [ ] Hover over the segments of the Doughnut Chart to trigger the Chart.js tooltips.
- [ ] Click the sidebar navigation items to show the hover highlights.

### Step 5: Conversational Prediction Wizard (1:45 - 2:30)
- [ ] Click "New Prediction" in the sidebar.
- [ ] Fill out the multi-step form:
  - **Step 1**: Select Gender, enter Age (e.g. 34), select Family Status. Click "Next".
  - **Step 2**: Enter Income (e.g. 45000), select Income Type. Click "Next".
  - **Step 3**: Enter Years Employed (e.g. 6), select Housing Type. Click "Next".
  - **Step 4**: Enter children count and debt. Click "Next" to see the review summary.
- [ ] Check that all entered values are listed correctly on the review step.
- [ ] Hover over the "Submit Application" button and click.

### Step 6: AI Scorecard & LIME Explanations (2:30 - 3:15)
- [ ] Wait 2 seconds for the result page to load.
- [ ] Let the circular progress approval probability gauge animate.
- [ ] Scroll down to the LIME Explainable AI section.
- [ ] Slowly hover over the horizontal support factors (green bars) and risk factors (red bars) to show the feature names and impact numbers.
- [ ] Scroll down to review the natural language recommendation summary.

### Step 7: Prediction History Logs & Printable Report (3:15 - 3:55)
- [ ] Click "Prediction History" in the sidebar.
- [ ] Enter the ID of the prediction you just made in the search box to verify the live filter query.
- [ ] Click "Print Report" on the target row.
- [ ] Let the printable assessment report open in a new tab.
- [ ] Scroll down the report, pausing briefly at the verification QR code.

### Step 8: Outro Slide (3:55 - 4:15)
- [ ] Stop recording, trim the screen capture files, and combine them with the generated `Intro.png` and `Outro.png` slides in your video editing software.
