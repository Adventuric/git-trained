## Git Repository Structure

Every Git project has four key areas:

| Area | Description |
|---|---|
| **Working Directory** | Where you write and edit code locally |
| **Staging Area (Index)** | Where you prepare changes before committing |
| **Local Repository** | Your local commit history (the `.git` folder) |
| **Remote Repository** | The central repo hosted on GitHub |

---

## Setup
```bash
git --version # Check Git is installed
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
---

### Started a new repo
```bash
mkdir git-trained
cd git-trained
git init
```

### To clone my repo
```bash
git clone https://github.com/Adventuric/git-trained
```

### Connect to a remote repo
```bash
git remote add origin https://github.com/Adventuric/git-trained
```

### Stage → Commit → Push
```bash
git add . # Staging all changes
git add -A # Stage all files and folders
git status # Check what's staged / untracked
git commit -m "your message" # Commit staged changes
git commit -a -m "your message" # Commiting without staging changes
git push <git-trained> main # Push to GitHub
```
---

## Branching

Work on features or fixes without touching the main codebase.

```bash
git branch <new-branch> # Create a branch
git checkout <new-branch> # Switch to it
# or do both at once:
git checkout -b <new-branch>

git branch # List all branches
git checkout main # Switch back to main
```

### Merging a branch
```bash
git checkout main
git merge <branch-name>
```

### Delete a branch
```bash
git branch -d <branch-name> # Safe delete (merged only)
git branch -D <branch-name> # Force delete
git push git-trained --delete <branch-name> # Delete from GitHub
```

---
## Stashing

Temporarily save uncommitted work so you can switch context.

```bash
git stash # Save changes, clean working dir
git stash save "label-name" # Stash with a label
git stash list # View all stashes
git stash clear # Delete all stashes
```

---

## Inspecting & Comparing

```bash
git status # See staged, unstaged, and untracked files
git log # View commit history
git diff # Compare working directory vs staging area
```

### Reverting a file to a previous commit
```bash
git checkout <commit-hash> file.txt
```
> Use `git log` to find the commit hash. `HEAD` always points to your latest commit.

---

## Ignoring Files

Create a `.gitignore` file to exclude logs, secrets, and build artifacts:

```bash
touch .gitignore
echo "*.log" >> .gitignore # Ignore all .log files
echo "node_modules/" >> .gitignore # Ignore node_modules folder
echo ".env" >> .gitignore # Ignore environment variables file
```

---

## Removing Files

```bash
git rm "filename" # Remove from repo and working directory
git rm --cached "filename" # Remove from staging only (keep local file)
```

---

## ↩ Undoing Changes

```bash
git checkout -f # Discard ALL uncommitted changes (use with caution)
```

---

## Quick Reference Cheat Sheet

| Command | What it does |
|---|---|
| `git init` | Initialize a new local repo |
| `git clone <url>` | Copy a remote repo locally |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Save a snapshot |
| `git push origin main` | Upload to GitHub |
| `git pull origin main` | Download + merge from GitHub |
| `git branch <name>` | Create a branch |
| `git checkout <branch>` | Switch branches |
| `git merge <branch>` | Merge branch into current |
| `git stash` | Temporarily save uncommitted work |
| `git log` | View commit history |
| `git diff` | Compare working dir vs staging |
| `git status` | Check current repo state |

---
