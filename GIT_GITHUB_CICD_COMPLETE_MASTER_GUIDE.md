# The Complete Git, GitHub & CI/CD Master Guide

A comprehensive, real-world handbook covering Git from fundamental concepts to enterprise branching strategies, the complete Git command encyclopedia, and GitHub Actions CI/CD automation using the **`git-cicd-retail-hub`** project.

---

## Table of Contents
1. [Core Conceptual Model: Git vs. GitHub](#1-core-conceptual-model-git-vs-github)
2. [The 4 Git Architecture Zones](#2-the-4-git-architecture-zones)
3. [The Complete Git Commands Encyclopedia](#3-the-complete-git-commands-encyclopedia)
   - [Setup & Configuration](#setup--configuration)
   - [Starting a Repository](#starting-a-repository)
   - [Basic Snapshotting & Staging](#basic-snapshotting--staging)
   - [Inspecting & Comparing Changes](#inspecting--comparing-changes)
   - [Branching & Switching](#branching--switching)
   - [Merging, Rebasing & Conflict Resolution](#merging-rebasing--conflict-resolution)
   - [Stashing (Temporary Shelving)](#stashing-temporary-shelving)
   - [Undoing Changes & Time Travel](#undoing-changes--time-travel)
   - [Remote Repositories & Collaboration](#remote-repositories--collaboration)
   - [Tagging & Releases](#tagging--releases)
   - [Advanced Auditing & Recovery](#advanced-auditing--recovery)
4. [Real-World Project Walkthrough (`git-cicd-retail-hub`)](#4-real-world-project-walkthrough-git-cicd-retail-hub)
5. [GitHub Actions CI/CD Complete Deep Dive](#5-github-actions-cicd-complete-deep-dive)
6. [Best Practices & Conventional Commits](#6-best-practices--conventional-commits)

---

## 1. Core Conceptual Model: Git vs. GitHub

| Dimension | Git | GitHub |
| :--- | :--- | :--- |
| **What is it?** | A command-line software tool for Distributed Version Control (VCS). | A cloud-based platform hosting Git repositories with web UI. |
| **Where it runs** | Locally on your computer (offline capable). | On Microsoft Azure cloud servers (online). |
| **Primary Job** | Tracks file modifications, snapshots commits, manages local branches. | Code hosting, Pull Requests (PRs), code reviews, Issues, CI/CD Actions. |
| **Network Need** | None needed to commit, branch, merge, diff, or check logs. | Internet needed to push, pull, fork, review PRs, and trigger Actions. |

---

## 2. The 4 Git Architecture Zones

```
 ┌──────────────────────┐
 │ 1. Working Directory │  Your actual folder with files on disk (untracked / modified)
 └──────────┬───────────┘
            │  git add <file>
            ▼
 ┌──────────────────────┐
 │ 2. Staging Area      │  The "Index" preparation zone of changes queued for snapshot
 └──────────┬───────────┘
            │  git commit -m "..."
            ▼
 ┌──────────────────────┐
 │ 3. Local Repository  │  The hidden .git/ directory storing permanent commit history
 └──────────┬───────────┘
            │  git push origin <branch>
            ▼
 ┌──────────────────────┐
 │ 4. Remote (GitHub)   │  The cloud repository shared across your team & CI/CD
 └──────────────────────┘
```

---

## 3. The Complete Git Commands Encyclopedia

### Setup & Configuration
Configures user identity, line endings, default branch names, and aliases.

- **`git config --global user.name "John Doe"`**
  - Sets the author name recorded in all future commits.
- **`git config --global user.email "john@example.com"`**
  - Sets author email address (must match your GitHub account for commit attribution).
- **`git config --global init.defaultBranch main`**
  - Sets `main` as the default name for newly initialized repositories instead of legacy `master`.
- **`git config --global core.autocrlf true`** (Windows) / `input` (macOS/Linux)
  - Automatically converts line endings to prevent Windows CRLF vs Unix LF discrepancies.
- **`git config --list --show-origin`**
  - Displays all active configuration settings along with the file path where each is stored.

---

### Starting a Repository
- **`git init`**
  - Initializes a new Git repository in the current folder by creating the hidden `.git/` metadata database.
- **`git clone <url>`**
  - Clones an entire remote repository from GitHub, downloads all historical branches/commits, and checks out `main`.
- **`git clone <url> <custom-folder-name>`**
  - Clones the remote repository into a custom destination directory name.
- **`git clone --depth 1 <url>`**
  - Performs a shallow clone downloading only the latest snapshot (great for fast CI/CD builds).

---

### Basic Snapshotting & Staging
- **`git status`**
  - Displays working tree status: untracked files, modified files, staged changes, and current branch.
- **`git status -s`**
  - Short-format status (`M` = modified, `A` = added/staged, `??` = untracked, `D` = deleted).
- **`git add <file>`**
  - Stages changes in `<file>` preparing it for the next commit.
- **`git add .`**
  - Stages all new, modified, and deleted files in the current directory tree.
- **`git add -p <file>`**
  - Interactive patch mode: prompts you chunk-by-chunk to selectively stage parts of a file.
- **`git commit -m "<message>"`**
  - Records the staged snapshot into the local repository with an informative description.
- **`git commit -am "<message>"`**
  - Automatically stages all tracked modified files AND commits them in a single command.
- **`git commit --amend`**
  - Modifies the most recent commit (updates message or includes newly staged files).

---

### Inspecting & Comparing Changes
- **`git diff`**
  - Shows line-by-line differences between your working directory and the staging area (unstaged edits).
- **`git diff --staged`** (or `git diff --cached`)
  - Shows line-by-line differences between your staged changes and the last commit.
- **`git diff branch-a..branch-b`**
  - Shows differences between two distinct branches.
- **`git log`**
  - Chronological commit history showing commit hash, author, date, and commit message.
- **`git log --oneline --graph --all`**
  - Compact ASCII branch tree visualization showing where branches diverge and merge.
- **`git log -n 5`**
  - Limits the output to the last 5 commits.
- **`git log -p <file>`**
  - Shows the full line-by-line diff history for a specific file across all commits.
- **`git show <commit-hash>`**
  - Shows the metadata and full diff introduced by a specific commit.
- **`git blame <file>`**
  - Displays each line of a file prefixed with the commit hash and author who last modified it.

---

### Branching & Switching
Branches enable parallel isolated workspaces for features, bug fixes, and experiments.

- **`git branch`**
  - Lists all local branches (the active branch is marked with `*` and highlighted).
- **`git branch -a`**
  - Lists all local AND remote tracking branches (`remotes/origin/...`).
- **`git branch <branch-name>`**
  - Creates a new branch at current HEAD without switching to it.
- **`git switch <branch-name>`** (Modern alternative to `git checkout`)
  - Switches your working directory to the target branch.
- **`git switch -c <branch-name>`** (or `git checkout -b <branch-name>`)
  - Creates a new branch AND switches to it immediately.
- **`git branch -d <branch-name>`**
  - Safely deletes a local branch (prevents deletion if branch contains unmerged changes).
- **`git branch -D <branch-name>`**
  - Force deletes a branch regardless of merge status.
- **`git branch -m <new-name>`**
  - Renames the current branch.

---

### Merging, Rebasing & Conflict Resolution
Combining changes from two branches.

- **`git merge <feature-branch>`**
  - Merges `<feature-branch>` into your active branch. Creates a merge commit if changes diverged (3-way merge).
- **`git merge --no-ff <feature-branch>`**
  - Forces a merge commit even if a fast-forward merge was possible (maintains feature history).
- **`git merge --abort`**
  - Aborts an in-progress merge conflict and restores the working tree back to pre-merge state.
- **`git rebase <target-branch>`**
  - Replays commits from the current branch on top of `<target-branch>`, producing a linear history.
- **`git rebase -i HEAD~3`**
  - Interactive rebase to squash, edit, reword, or drop the last 3 commits.
- **`git cherry-pick <commit-hash>`**
  - Copies a specific commit from any branch and applies it onto the current active branch.

---

### Stashing (Temporary Shelving)
Saves uncommitted work without committing so you can switch branches or pull cleanly.

- **`git stash`** (or `git stash push -m "work in progress"`)
  - Shelves all modified tracked files into a temporary stash stack.
- **`git stash -u`**
  - Stashes modified files AND untracked new files.
- **`git stash list`**
  - Lists all saved stashes (`stash@{0}`, `stash@{1}`).
- **`git stash pop`**
  - Restores the most recent stash and removes it from the stack.
- **`git stash apply`**
  - Restores the most recent stash while keeping it on the stash stack.
- **`git stash drop stash@{0}`**
  - Discards a specific stash from the stack.
- **`git stash clear`**
  - Wipes out all saved stashes.

---

### Undoing Changes & Time Travel
- **`git restore <file>`**
  - Discards unstaged modifications in the working directory, restoring file to last commit state.
- **`git restore --staged <file>`**
  - Unstages a file, moving changes back to unstaged working directory.
- **`git revert <commit-hash>`**
  - Creates a brand new commit that inverses the changes of `<commit-hash>` (safe for public branches).
- **`git reset --soft HEAD~1`**
  - Undoes the last commit but leaves all files staged in the index (no code lost).
- **`git reset --mixed HEAD~1`** (default reset)
  - Undoes the last commit and unstages files (leaves changes in working directory).
- **`git reset --hard HEAD~1`**
  - **DANGEROUS**: Completely deletes the last commit and discards all changes.
- **`git clean -fd`**
  - Removes untracked files (`-f`) and untracked directories (`-d`) from the working directory.

---

### Remote Repositories & Collaboration
- **`git remote add origin <url>`**
  - Connects your local repository to a remote repository hosted on GitHub.
- **`git remote -v`**
  - Lists all registered remote names and their fetch/push URLs.
- **`git remote set-url origin <new-url>`**
  - Updates the URL of an existing remote.
- **`git push -u origin <branch>`**
  - Pushes your local branch commits to GitHub and sets upstream tracking (`-u`).
- **`git push`**
  - Pushes commits on the current branch to its configured upstream remote.
- **`git fetch origin`**
  - Downloads new commits and branches from GitHub into local tracking without modifying your working files.
- **`git pull origin <branch>`**
  - Fetches changes from GitHub and immediately merges them into the current branch (`fetch` + `merge`).
- **`git pull --rebase origin <branch>`**
  - Fetches changes and rebases local unpushed commits on top of remote changes.

---

### Tagging & Releases
Tags mark specific points in repository history as important (releases, versions).

- **`git tag`**
  - Lists all tags in the repository.
- **`git tag -a v1.0.0 -m "Release version 1.0.0"`**
  - Creates an annotated tag with author, date, and release notes.
- **`git push origin v1.0.0`**
  - Pushes a specific tag to GitHub (triggers GitHub Releases & CI/CD workflows).
- **`git push origin --tags`**
  - Pushes all local tags to GitHub.
- **`git tag -d v1.0.0`**
  - Deletes a local tag.

---

### Advanced Auditing & Recovery
- **`git reflog`**
  - Git's internal safety net: records every single movement of HEAD (commits, checkouts, resets, rebase).
  - Even if you run `git reset --hard`, you can recover lost commits by finding the hash in `reflog`!

---

## 4. Real-World Project Walkthrough (`git-cicd-retail-hub`)

Let’s trace the active repository located in `c:\Users\2869026\Desktop\visual\git-cicd-retail-hub`.

### Project Structure
```
git-cicd-retail-hub/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          <-- GitHub Actions CI/CD Pipeline
├── src/
│   └── retail_calc.py         <-- Core calculation microservice
├── tests/
│   └── test_retail_calc.py    <-- Unit test suite
├── .gitignore                 <-- Protects venv, pycache, .env
├── requirements.txt           <-- Python dependencies
└── README.md                  <-- Project documentation & badges
```

### Try these real Git commands right now in your terminal:

```bash
cd c:\Users\2869026\Desktop\visual\git-cicd-retail-hub

# 1. Inspect status
git status

# 2. View commit history
git log --oneline --graph --all

# 3. Switch between branches
git switch main
git switch feature/bulk-tier-discount

# 4. Run tests
python -m unittest discover -s tests -v

# 5. Create an annotated release tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial stable pricing engine"
git tag
```

---

## 5. GitHub Actions CI/CD Complete Deep Dive

Located in [`.github/workflows/ci-cd.yml`](file:///c:/Users/2869026/Desktop/visual/git-cicd-retail-hub/.github/workflows/ci-cd.yml).

### The CI/CD Architecture
```
 [Code Pushed to GitHub]
            │
            ▼
 ┌────────────────────────────────────────────────┐
 │ Job 1: Linting (flake8)                        │
 │ - Runs on ubuntu-latest                        │
 │ - Validates code syntax, line lengths, imports │
 └──────────────────┬─────────────────────────────┘
                    │ (needs: lint)
                    ▼
 ┌────────────────────────────────────────────────┐
 │ Job 2: Automated Testing (Matrix Strategy)     │
 │ - Tests Python 3.10, 3.11, and 3.12 in parallel│
 │ - Runs: python -m unittest discover -s tests   │
 └──────────────────┬─────────────────────────────┘
                    │ (needs: test, if: tag v*)
                    ▼
 ┌────────────────────────────────────────────────┐
 │ Job 3: Build & Release Package                 │
 │ - Builds wheel and tar.gz distributions        │
 │ - Uploads release artifacts to GitHub          │
 └────────────────────────────────────────────────┘
```

### Workflow Code Breakdown:
1. **Triggers (`on:`)**:
   ```yaml
   on:
     push:
       branches: [ main, develop ]
       tags: [ 'v*' ]
     pull_request:
       branches: [ main ]
   ```
   *Runs automatically on pull requests to `main`, pushes to `main`, and when a release tag (e.g. `v1.0.0`) is pushed.*

2. **Matrix Strategy (`strategy.matrix`)**:
   ```yaml
   strategy:
     matrix:
       python-version: ["3.10", "3.11", "3.12"]
   ```
   *Spawns 3 parallel runners ensuring the code is compatible across multiple Python versions.*

3. **Conditional Deployment (`if:`)**:
   ```yaml
   if: startsWith(github.ref, 'refs/tags/v')
   ```
   *Ensures packaging only happens when an official release tag is cut, preventing untested commits from deploying.*

---

## 6. Best Practices & Conventional Commits

Use standard commit prefixes for clean, professional change logs:

| Prefix | Usage | Example |
| :--- | :--- | :--- |
| **`feat:`** | A new feature | `feat: add Texas state sales tax calculator` |
| **`fix:`** | A bug fix | `fix: resolve discount rounding error in cart total` |
| **`docs:`** | Documentation changes | `docs: add installation and setup instructions` |
| **`test:`** | Adding or updating tests | `test: add unit test for zero-quantity items` |
| **`refactor:`** | Code refactoring without changing behavior | `refactor: extract coupon calculation into helper method` |
| **`ci:`** | CI/CD pipeline modifications | `ci: add Python 3.12 to GitHub Actions matrix` |
