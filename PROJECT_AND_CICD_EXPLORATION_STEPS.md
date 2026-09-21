# Project Overview & Step-by-Step Guide for Exploring Git, GitHub & CI/CD

This document explains everything about the **`git-cicd-retail-hub`** project, its architecture, and provides a clear, step-by-step roadmap to explore every Git command, GitHub collaboration feature, and GitHub Actions CI/CD pipeline.

---

## 1. Project Explanation: `git-cicd-retail-hub`

### What is this Project?
**Retail Hub Pricing Engine** is a production-grade Python **FastAPI microservice** designed to handle enterprise checkout calculations, promotional coupons, bulk quantity discount tiers, and multi-state US sales tax.

It was built intentionally as a clean, complete, test-driven application so that:
1. **Right Now**: You can use it to practice the complete Git lifecycle, branching, Pull Requests, merge conflicts, and automated GitHub Actions CI/CD pipelines.
2. **Next Step**: The exact same codebase is already container-ready (`Dockerfile`, `docker-compose.yml`) so you can seamlessly transition into Docker builds, image registries (ACR), and cloud container deployments (Azure Container Apps / Kubernetes).

---

### Project File Structure

```
git-cicd-retail-hub/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD Pipeline (Lint, Test Matrix, Build)
│
├── src/
│   ├── main.py                # FastAPI Application & REST API Endpoints
│   ├── models.py              # Pydantic Request/Response Data Schemas
│   └── retail_calc.py         # Pure Calculation Engine (Subtotal, Coupons, Tax, Bulk Tiers)
│
├── tests/
│   ├── test_retail_calc.py    # Unit tests for pure calculation business logic
│   └── test_api.py            # Integration tests for FastAPI HTTP endpoints
│
├── Dockerfile                 # Multi-stage, non-root production container recipe
├── .dockerignore              # Prevents unnecessary files from bloating container images
├── docker-compose.yml         # Single-command local container execution
├── .gitignore                 # Prevents Python bytecode and .env secrets from Git
├── requirements.txt           # Application dependencies (FastAPI, Uvicorn, Flake8, etc.)
└── README.md                  # Project documentation, badges, and quickstart
```

---

### Key Endpoints & Capabilities

| Endpoint | Method | Purpose |
| :--- | :--- | :--- |
| **`/health`** | `GET` | Container health probe for Kubernetes & Azure Container Apps |
| **`/api/v1/catalog`** | `GET` | Returns available store items (Headphones, Laptops, Chargers) |
| **`/api/v1/promos/validate`** | `POST` | Validates coupons (`WELCOME10`, `VIP20`, `FLASH50`) |
| **`/api/v1/checkout`** | `POST` | Itemized invoice calculation with bulk discount & sales tax |
| **`/docs`** | `GET` | Interactive Swagger UI API documentation |

---

## 2. Step-by-Step Guide to Explore Git, GitHub & CI/CD

Follow these steps in order to experience the full developer lifecycle.

---

### Step 1: Verify Your Local Repository Health

Open a terminal in the project directory:
```bash
cd c:\Users\2869026\Desktop\visual\git-cicd-retail-hub
```

1. **Check Git Status**:
   ```bash
   git status
   ```
   *Expected*: `On branch main`, `nothing to commit, working tree clean`.

2. **Run Local Automated Tests**:
   ```bash
   python -m unittest discover -s tests -v
   ```
   *Expected*: All 14 tests pass (`OK`).

3. **Inspect the Local Commit History**:
   ```bash
   git log --oneline --graph --all
   ```

---

### Step 2: Create a New Remote Repository on GitHub

1. Open your browser and go to **[GitHub.com](https://github.com)**.
2. Click the **`+`** icon at the top right and select **New repository**.
3. Fill in:
   - **Repository Name**: `retail-pricing-engine` (or any name you choose)
   - **Visibility**: `Public` (recommended for unlimited free CI/CD runner minutes)
   - ⚠️ **Important**: Leave all initialization boxes **UNCHECKED**:
     - Do NOT add README
     - Do NOT add .gitignore
     - Do NOT add license  
     *(Your local project already has all of these!)*
4. Click **Create repository**.
5. Copy your repository URL, e.g.:
   `https://github.com/<your-username>/retail-pricing-engine.git`

---

### Step 3: Connect Local Git to GitHub and Push

In your terminal:

```bash
# 1. Ensure you are on the main branch
git switch main

# 2. Add the remote GitHub link (replace with your actual GitHub URL)
git remote add origin https://github.com/<your-username>/retail-pricing-engine.git

# 3. Verify the remote connection
git remote -v

# 4. Push your code and set upstream tracking (-u)
git push -u origin main
```
*(When prompted by the Git Credential Manager, sign in via browser or personal access token)*.

---

### Step 4: Watch Your First CI/CD Pipeline Run Live on GitHub!

1. Open your repository on **GitHub.com**.
2. Click the **"Actions"** tab at the top.
3. You will see the **`Retail Hub CI/CD Pipeline`** in progress!
4. Click on the run to view the live execution:
   - **Job 1: Linting**: Checks code quality and syntax with `flake8`.
   - **Job 2: Unit Testing Matrix**: Runs tests simultaneously on **Python 3.10, 3.11, and 3.12** across parallel virtual machines!
5. When both jobs finish with green checkmarks (`Passed`), your code is verified for production.

---

### Step 5: Practice the Professional Feature Branch Workflow

In enterprise teams, developers **never commit directly to `main`**. They create a feature branch, make changes, and open a Pull Request (PR).

Let's add a new feature: **Georgia State Sales Tax (`GA: 0.0400`)**.

1. **Create and switch to a new branch**:
   ```bash
   git switch -c feature/add-georgia-tax
   ```

2. **Verify your active branch**:
   ```bash
   git branch
   ```
   *(You will see an asterisk `*` next to `feature/add-georgia-tax`)*.

---

### Step 6: Make Code Changes & Run Local Tests

1. Open `src/retail_calc.py` and add `"GA": 0.0400` inside `tax_rates`:
   ```python
   tax_rates = {
       "TX": 0.0825,
       "CA": 0.0925,
       "NY": 0.08875,
       "IL": 0.0875,
       "FL": 0.0600,
       "GA": 0.0400
   }
   ```

2. Open `tests/test_retail_calc.py` and add a unit test:
   ```python
   def test_sales_tax_ga(self):
       tax = calculate_sales_tax(100.00, "GA")
       self.assertEqual(tax, 4.00)
   ```

3. Run the test suite to ensure the new feature passes:
   ```bash
   python -m unittest discover -s tests -v
   ```
   *(15 tests should now pass!)*

---

### Step 7: Stage and Commit the New Feature

1. **Inspect line-by-line differences**:
   ```bash
   git diff
   ```
2. **Stage the modified files**:
   ```bash
   git add src/retail_calc.py tests/test_retail_calc.py
   ```
3. **Commit with a descriptive message**:
   ```bash
   git commit -m "feat: add Georgia state sales tax rate calculation"
   ```

---

### Step 8: Push the Branch and Open a Pull Request (PR)

1. **Push the feature branch to GitHub**:
   ```bash
   git push -u origin feature/add-georgia-tax
   ```

2. **Open the Pull Request on GitHub**:
   - Go to your repository on **GitHub.com**.
   - GitHub will display a yellow notification: **`feature/add-georgia-tax had recent pushes`**.
   - Click the green button: **"Compare & pull request"**.
   - Click **"Create pull request"**.

3. **Watch GitHub Actions Validate Your PR**:
   - Scroll down on the PR page.
   - GitHub Actions will automatically start running your linting and testing jobs against your Pull Request.
   - Once all checks are green: **"All checks have passed"**.

4. **Merge the Pull Request**:
   - Click **"Merge pull request"** -> **"Confirm merge"**.
   - Click **"Delete branch"** on GitHub.

---

### Step 9: Synchronize Your Local Repository

Now that GitHub has merged your branch into `main`, sync your local machine:

```bash
# 1. Switch back to your local main branch
git switch main

# 2. Download and merge the latest commits from GitHub
git pull origin main

# 3. Delete the local feature branch that is already merged
git branch -d feature/add-georgia-tax

# 4. View your updated commit tree
git log --oneline --graph
```

---

### Step 10: Cut a Production Release Tag (Trigger Deployment)

Version tags mark milestones (e.g. `v1.0.0`). Pushing a release tag triggers the **Build & Package** job in your CI/CD pipeline:

```bash
# 1. Create an annotated release tag
git tag -a v1.0.0 -m "Release v1.0.0: Enterprise Retail Pricing Microservice"

# 2. Push the tag to GitHub
git push origin v1.0.0
```

1. Go to the **Actions** tab on GitHub.
2. Notice that **Job 3: Build & Package Artifacts** has triggered!
3. When it finishes, you can download the built distribution packages (`.whl` and `.tar.gz`) directly from the **Artifacts** section of the run.

---

## 3. Next Phase: Docker & Azure Cloud Deployment

The repository is already equipped with:
- **`Dockerfile`**: Multi-stage, non-root, secure container build.
- **`docker-compose.yml`**: Easy local multi-service container testing.

When you are ready for containerization and deployment:
1. **Run locally with Docker**:
   ```bash
   docker build -t retail-pricing-engine:latest .
   docker run -d -p 8000:8000 retail-pricing-engine:latest
   ```
2. **Access Swagger UI**: `http://localhost:8000/docs`
3. **Deploy to Azure**:
   - Tag and push to Azure Container Registry (ACR): `acrexploreai65064.azurecr.io`
   - Deploy serverless on Azure Container Apps (ACA) in resource group `rg-explore-ai`.
