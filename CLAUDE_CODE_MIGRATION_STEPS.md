# Claude Code Migration: NPM to Native Binary

**Current Status**: NPM installation v2.0.33 with file locks

**Goal**: Migrate to native binary installation

---

## Migration Steps (Execute After Closing Claude Code)

### Step 1: Close All Claude Code Sessions
- Close this Claude Code window
- Close any other Claude Code windows/terminals
- Wait 10 seconds for processes to fully terminate

### Step 2: Verify Processes Are Closed
Open Git Bash or CMD and run:
```bash
tasklist | findstr claude
```
If any processes remain, note the PIDs and run:
```cmd
taskkill /F /PID [process_id]
```

### Step 3: Uninstall NPM Version
Open Git Bash or CMD and run:
```bash
npm uninstall -g @anthropic-ai/claude-code
```

Verify removal:
```bash
npm list -g | grep claude
```
Should return nothing.

### Step 4: Download Native Binary
1. Open browser and go to: https://claude.ai/download
2. Download the Windows installer (claude-code-setup.exe)
3. Save to Downloads folder

### Step 5: Install Native Binary
1. Navigate to Downloads folder
2. Double-click `claude-code-setup.exe`
3. Follow installation wizard
4. Default installation path: `C:\Users\BrettWalker\AppData\Local\Programs\claude-code\`

### Step 6: Verify Installation
Open a NEW Git Bash or CMD window and run:
```bash
which claude
# Should show: /c/Users/BrettWalker/AppData/Local/Programs/claude-code/claude.exe

claude --version
# Should show: 2.0.33 or newer (native)
```

---

## Benefits of Native Installation

✅ **No Node.js Dependency**: Runs as standalone executable
✅ **Faster Startup**: No NPM overhead
✅ **Better Auto-Updater**: More reliable update mechanism
✅ **Cleaner Installation**: Single executable vs NPM modules

---

## Troubleshooting

### NPM Uninstall Fails with "EBUSY"
- Ensure ALL Claude Code windows are closed
- Run `tasklist | findstr claude` to verify
- Force kill any remaining processes
- Try uninstall again

### Native Installer Doesn't Run
- Right-click installer → "Run as Administrator"
- Check Windows Defender hasn't blocked it
- Temporarily disable antivirus if needed

### PATH Not Updated After Install
- Close and reopen Git Bash/CMD
- Or manually add to PATH: `C:\Users\BrettWalker\AppData\Local\Programs\claude-code\`

---

## Current Environment Info

**OS**: Windows 10.0.26100 (MINGW64_NT)
**Current Claude**: NPM v2.0.33 at `/c/Users/BrettWalker/AppData/Roaming/npm/claude`
**Node.js**: v24.4.1
**NPM**: Installed
**Git Bash**: Available

**Active Claude Processes**: 13 (this session + background tasks)

---

## Next Steps

1. **Save this file** for reference
2. **Close Claude Code** (this window)
3. **Follow Steps 1-6** above
4. **Reopen Claude Code** in Git Bash with `claude` command

**Estimated Time**: 5-10 minutes

---

**Created**: November 5, 2025
**Purpose**: Manual migration from NPM to native Claude Code installation
