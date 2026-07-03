# Screen Recording Checklist

Ensure all items are verified before completing the recording session.

---

### 1. Environment Setup Checklist
- [ ] Flask server is running in `production` mode with debug active (`python app/app.py`).
- [ ] Database contains at least 15+ mock prediction records across different risk profiles to show charts populate fully.
- [ ] Logged-in user is created with a clean test name.

### 2. Audio & Video Quality Checklist
- [ ] Resolution: 1920x1080 (1080p) or higher.
- [ ] Audio: Clean voiceover, zero static, clear pacing.
- [ ] Frame Rate: Minimum 30 FPS, recommended 60 FPS.
- [ ] Browser window is maximized; all tabs, bookmark bars, and OS taskbars are hidden for a clean view.

### 3. Execution Flow Checklist
- [ ] Theme toggle shown (Light Mode -> Dark Mode).
- [ ] New application submitted, gauge animation finishes, and XAI feature attributions are shown.
- [ ] Table filtering works, and page numbers click through correctly.
- [ ] CSV file exports successfully.
- [ ] Chart timeline toggle updates the line chart labels and data dynamically.
- [ ] Print window triggered, showing the printable page styling correctly.
- [ ] Log out successfully redirects user to landing page.
