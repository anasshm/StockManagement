# Recording & Replay Guide

## 🎯 Purpose

This system lets you record real browser actions and replay them. It solves the problem where the automation can't find elements that you can clearly see - by recording what you actually do, we capture the working selectors and actions.

## 📋 Quick Start

### Step 1: Record Your Session
```bash
python3 record_session.py
```

**What happens:**
- Two windows open: Browser + Inspector
- You perform your normal workflow in the browser
- Inspector shows generated Python code in real-time
- When done, copy ALL the code from Inspector

### Step 2: Save the Recorded Code
1. Open `automation/analytics_recorded.py`
2. Find the `replay_actions()` function
3. Replace the `TODO` comment with your copied code
4. Save the file

### Step 3: Test the Replay
```bash
python3 replay_recorded_session.py
```

**What happens:**
- Browser opens and replays your actions
- Creates a trace file with screenshots
- Shows if the recording works correctly

### Step 4: View the Visual Playbook
```bash
python3 view_trace.py
```

**What you see:**
- Timeline of every action
- Screenshots at each step
- DOM state at each point
- Network requests
- Element selectors that worked

## 📁 Files

| File | Purpose |
|------|---------|
| `record_session.py` | Launches recording tool |
| `view_trace.py` | Opens trace viewer |
| `automation/analytics_recorded.py` | Your recorded actions (edit this) |
| `replay_recorded_session.py` | Runs the replay |
| `traces/analytics_session.zip` | Visual recording (generated) |

## 🔄 Complete Workflow

```
1. Record
   python3 record_session.py
   → Do your actions in browser
   → Copy generated code

2. Save
   → Paste code into automation/analytics_recorded.py
   → Replace the TODO section

3. Replay
   python3 replay_recorded_session.py
   → Watch it replay your actions
   → Creates trace file

4. Debug
   python3 view_trace.py
   → See exactly what happened
   → Check which selectors worked
   → Compare with failed automation

5. Extract
   → Copy working selectors
   → Update main automation (codpartner.py)
   → Use trace as reference when debugging
```

## 💡 Use Cases

### Debugging Date Selection
If the main automation can't select dates:
1. Record yourself selecting dates successfully
2. View the trace to see working selectors
3. Copy those selectors to `codpartner.py`

### Testing New Workflows
Before automating something new:
1. Record it manually first
2. Verify the replay works
3. Extract the code
4. Add error handling and logic

### Documentation
The trace serves as visual documentation:
- Shows exactly how the UI works
- Captures element names/IDs that work
- Provides screenshots for reference

### When Website Changes
If automation breaks:
1. Record the new workflow
2. Compare old vs new trace
3. See what changed
4. Update selectors

## 🎬 Example Recording Session

Let's say you want to record the analytics download:

```bash
# Start recording
python3 record_session.py
```

**In the browser that opens:**
1. Login with your credentials
2. Click on "Reports" or navigate to analytics
3. Click "Saudi Arabia" button
4. Click "Filter" button
5. Click date picker
6. Select start date
7. Select end date
8. Click "Apply" (in date picker)
9. Click "Apply" (in filter dialog)
10. Wait for data to load

**In the Inspector window:**
- Watch as Python code appears for each action
- When finished, click the "Copy" button or select all code

**Paste into `automation/analytics_recorded.py`:**
```python
def replay_actions(page: Page):
    # Paste the copied code here
    page.goto("https://app.codpartner.com/login")
    page.fill('input[name="email"]', "your@email.com")
    page.fill('input[name="password"]', "your_password")
    page.click('button:has-text("Log In")')
    # ... all your recorded actions
```

**Test it:**
```bash
python3 replay_recorded_session.py
```

**View results:**
```bash
python3 view_trace.py
```

## 🔍 Troubleshooting

### No code appears in Inspector
- Make sure you're interacting with the browser window (not the Inspector)
- Try clicking visible buttons/links first
- Check that Playwright is installed: `playwright --version`

### Replay fails
- Check credentials in `.env` file
- Verify you copied ALL the code (including imports if any)
- Look at the trace to see where it failed

### Trace file not found
- Make sure you ran `replay_recorded_session.py` first
- Check that `traces/` directory exists
- Look for error messages during replay

### "TODO" error when replaying
- You need to paste recorded code into `analytics_recorded.py`
- Run `record_session.py` first to generate code

## 🎓 Tips

1. **Record in chunks**: Don't record everything at once. Record login separately from analytics, etc.

2. **Add waits**: If actions happen too fast, add `page.wait_for_timeout(1000)` in the recorded code

3. **Remove credentials**: After recording, replace hardcoded email/password with variables:
   ```python
   from .config import Config
   config = Config()
   page.fill('input[name="email"]', config.USERNAME)
   ```

4. **Keep recordings**: Save multiple versions - date_selection.py, login.py, etc.

5. **Compare traces**: Keep traces from successful runs to compare with failed runs

## 🚀 Next Steps

After you have working recorded actions:

1. **Extract patterns**: See what selectors consistently work
2. **Update main automation**: Copy working code to `codpartner.py`
3. **Add error handling**: The recorded version is "dumb" - add retries, checks, etc.
4. **Parameterize**: Make dates, countries, etc. into variables
5. **Keep the recording**: Use as reference when debugging

---

**Remember**: The recorded version is a "playbook" - it shows what works. The main automation (`codpartner.py`) should use these working patterns but add logic, error handling, and flexibility.

