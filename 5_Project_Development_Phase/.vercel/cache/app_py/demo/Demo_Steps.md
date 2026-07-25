# Demo Recording Steps

Follow these precise steps to record the platform demo video.

---

### Step 1: Initialization
1. Launch the local Flask server on port `5000` via `python app/app.py`.
2. Clear the browser cache and load the home page: `http://localhost:5000`.
3. Open screen recording software (OBS, Loom, QuickTime) set to `1080p` at `60 FPS`.

---

### Step 2: Show Landing Page (0:00 - 0:30)
1. Start recording with the landing page visible in dark mode.
2. Slowly scroll down to reveal the 3D rotating Credit Card, stats panel, features section, and tech stack.
3. Scroll back up and click "Get Started".

---

### Step 3: Register & Login (0:30 - 1:00)
1. Fill in registration details on `/auth/register` (use a demo username like `demouser`).
2. Submit the form, redirecting to `/auth/login`.
3. Log in with the registered credentials to reveal the premium sidebar dashboard.

---

### Step 4: Run Application Assessment (1:00 - 2:00)
1. Click "New Application" in the sidebar.
2. Complete Step 1: Personal Info. Hover over inputs to show tooltip indicators, click Next.
3. Complete Step 2: Financial Info. Check "unemployed" and change parameters to show form validations. Uncheck and enter stable credentials (e.g. $90k income), click Next.
4. Review parameters on Step 3, click Next.
5. Click "Submit Application" on Step 4.

---

### Step 5: Explain Decision & XAI (2:00 - 2:45)
1. Let the gauge countup animation complete.
2. Hover over feature weights on the positive/negative LIME factor cards.
3. Read the natural language suggestions card.

---

### Step 6: History Table & Analytics (2:45 - 3:30)
1. Click "Prediction History" in the sidebar.
2. Filter columns by clicking "Approved Only", then search for `demouser` profiles.
3. Click "Export CSV" to show file downloading.
4. Click "Dashboard" in the sidebar. Highlight the Chart.js visual metrics, click "Monthly" toggle on the prediction line timeline.

---

### Step 7: Print Report & Logout (3:30 - 4:00)
1. Go back to History, click "Report" on the latest entry.
2. Show the printable layout and QR verification code.
3. Trigger print (`Ctrl + P`) to show PDF saving options. Cancel the print dialog.
4. Click "Log Out" in the sidebar footer. Stop recording.
