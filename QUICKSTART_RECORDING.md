# Quick Start: Record Your First Session

Follow these steps to record and replay your analytics workflow.

## Prerequisites

Make sure Playwright is installed:
```bash
playwright --version
```

If not installed:
```bash
pip3 install playwright
playwright install chromium
```

## Step-by-Step Guide

### 1️⃣ Start Recording (2 minutes)

```bash
python3 record_session.py
```

**Two windows will open:**
- **Browser window** (left) - Interact here
- **Inspector window** (right) - Shows generated code

### 2️⃣ Perform Your Workflow (5 minutes)

In the **browser window**, do your normal routine:

1. ✅ Enter email and password
2. ✅ Click "Log In"
3. ✅ Navigate to Analytics page (or it might auto-navigate)
4. ✅ Click "Saudi Arabia" button
5. ✅ Click "Filter" button
6. ✅ Click on the date range input
7. ✅ Select your start date
8. ✅ Select your end date
9. ✅ Click "Apply" (in date picker)
10. ✅ Click "Apply" (in filter dialog if there's a second one)
11. ✅ Wait for data to load

**Watch the Inspector window** - Python code appears as you interact!

### 3️⃣ Copy the Generated Code (1 minute)

In the **Inspector window**:
1. Click the "Copy" button (top right)
2. OR select all the code (Cmd+A) and copy (Cmd+C)

**Close both windows when done.**

### 4️⃣ Save the Code (2 minutes)

1. Open `automation/analytics_recorded.py` in your editor
2. Find the `replay_actions()` function
3. Look for this comment:
   ```python
   # TODO: PASTE YOUR RECORDED ACTIONS HERE
   ```
4. **Replace the TODO section** with your copied code
5. Save the file

**Example of what to paste:**
```python
def replay_actions(page: Page):
    page.goto("https://app.codpartner.com/login")
    page.fill('input[name="email"]', "your@email.com")
    page.fill('input[name="password"]', "your_password")
    page.click('button:has-text("Log In")')
    page.click('text="Saudi arabia"')
    # ... rest of your actions
```

### 5️⃣ Test the Replay (1 minute)

```bash
python3 replay_recorded_session.py
```

**What you'll see:**
- Browser opens
- Your actions replay automatically
- A trace file is saved: `traces/analytics_session.zip`

### 6️⃣ View the Visual Playbook (2 minutes)

```bash
python3 view_trace.py
```

**Explore the trace viewer:**
- 📸 Screenshots of every action
- 🔍 Inspect elements at each step
- 📊 See network requests
- ✅ Verify which selectors worked

## 🎉 Success!

You now have:
- ✅ Working recorded code
- ✅ Visual trace with screenshots
- ✅ Reference for debugging
- ✅ Exact selectors that work

## 🔧 Next Steps

### Extract Working Selectors

Open the trace viewer and look for:
- Date picker selectors
- Button selectors
- Filter dialog selectors

Copy these to update `automation/codpartner.py` if needed.

### Remove Hardcoded Credentials

In `automation/analytics_recorded.py`, replace:
```python
page.fill('input[name="email"]', "your@email.com")
page.fill('input[name="password"]', "your_password")
```

With:
```python
from .config import Config
config = Config()
page.fill('input[name="email"]', config.USERNAME)
page.fill('input[name="password"]', config.PASSWORD)
```

### Record Different Workflows

Run `record_session.py` again to record:
- Different date ranges
- Different countries
- Different pages (Orders, Inventory, etc.)

Save each as a different file:
- `automation/analytics_recorded.py`
- `automation/orders_recorded.py`
- `automation/inventory_recorded.py`

## 💡 Tips

1. **Go slow** during recording - give pages time to load
2. **Add waits** in code if replay is too fast:
   ```python
   page.wait_for_timeout(2000)  # Wait 2 seconds
   ```
3. **Record in chunks** - don't try to record everything at once
4. **Keep traces** - they're great debugging references

## ❓ Troubleshooting

**Problem: Inspector shows no code**
- Solution: Make sure you're clicking in the browser window, not the Inspector

**Problem: Replay fails at login**
- Solution: Check `.env` file has correct credentials

**Problem: Trace file not found**
- Solution: Run `replay_recorded_session.py` first to create the trace

**Problem: Can't view trace**
- Solution: Run `playwright install` to install browsers

## 📚 More Help

See [RECORDING_GUIDE.md](RECORDING_GUIDE.md) for detailed documentation.

---

**Ready to record? Run:** `python3 record_session.py` 🎬

