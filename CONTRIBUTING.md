# How to Update This Project

## Quick Git Workflow

### After Making Changes

1. **Check what changed:**
```bash
git status
```

2. **Stage your changes:**
```bash
git add .
```

3. **Commit with a message:**
```bash
git commit -m "Description of what you changed"
```

4. **Push to GitHub:**
```bash
git push
```

### Example Workflow

```bash
# Made improvements to compare_inventory.py
git add compare_inventory.py
git commit -m "Add support for handling negative stock values"
git push
```

## Good Commit Message Examples

✅ Good:
- `"Fix: Handle empty product names in parser"`
- `"Add: Support for multiple warehouses in same file"`
- `"Update: README with new usage examples"`
- `"Improve: CSV column headers with dynamic dates"`

❌ Avoid:
- `"Update"`
- `"Fix bug"`
- `"Changes"`

## Development Tips

1. **Test locally first** - Always run the script before committing
2. **Commit often** - Small, focused commits are better
3. **One feature at a time** - Don't mix multiple changes in one commit
4. **Update README** - If you add features, document them

## File Organization

**Tracked in Git (code):**
- `compare_inventory.py` - Main script
- `README.md` - Documentation
- `SETUP.md` - Setup guide
- `.gitignore` - Git ignore rules

**NOT tracked (data):**
- `*.html` - Your inventory files
- `*.csv` - Generated reports
- These are in `.gitignore` and won't be pushed to GitHub

## Useful Git Commands

```bash
# See recent commits
git log --oneline -5

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See what changed in a file
git diff compare_inventory.py

# Pull latest changes from GitHub
git pull
```

---

**Remember:** Your HTML and CSV files stay local. Only code goes to GitHub! 🚀
