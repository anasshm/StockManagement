# Daily Automation Setup

This guide shows how to set up automatic daily stock updates that run once every 24 hours after you log into your Mac.

## How It Works

- **Runs automatically** once every 24 hours after you log in
- **Downloads** today's inventory
- **Compares** with yesterday
- **Creates** your CSV report
- **Runs in background** (headless/invisible)
- **Logs** all output to `logs/` folder

## Installation

**One-time setup:**

```bash
cd "/Users/zak/Downloads/Stock management"
./setup_automation.sh
```

That's it! ✅

## What Happens Now

1. You log into your Mac (any time: 5 AM, 5 PM, whenever)
2. Within a few seconds, the script runs automatically in the background
3. Your `Stock_OCT04.csv` report is generated
4. It won't run again for 24 hours

## Check If It's Working

**View the logs:**

```bash
# See the output
cat logs/stock_update.log

# See any errors
cat logs/stock_update_error.log
```

**Check status:**

```bash
launchctl list | grep stockmanagement
```

If you see output, it's running!

## Manual Run Anytime

You can still run it manually whenever you want:

```bash
python3 stock_update.py
```

This won't interfere with the automatic schedule.

## Disable Automation

If you want to stop the automatic runs:

```bash
./disable_automation.sh
```

You can re-enable it anytime by running `./setup_automation.sh` again.

## Troubleshooting

### Script didn't run automatically

1. Check if it's loaded:
   ```bash
   launchctl list | grep stockmanagement
   ```

2. Check the error log:
   ```bash
   cat logs/stock_update_error.log
   ```

3. Try manual run to test:
   ```bash
   python3 stock_update.py
   ```

### Need to change the schedule

Edit `com.stockmanagement.daily.plist`:
- `StartInterval` is in seconds
- `86400` = 24 hours
- `43200` = 12 hours
- `3600` = 1 hour

Then reload:
```bash
./setup_automation.sh
```

## Files

- `com.stockmanagement.daily.plist` - Mac automation config
- `setup_automation.sh` - Install the automation
- `disable_automation.sh` - Remove the automation
- `logs/stock_update.log` - Normal output
- `logs/stock_update_error.log` - Error messages

---

**Set it and forget it! 🚀**

