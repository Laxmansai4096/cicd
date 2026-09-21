# Hands-On Lab: Practice Git, GitHub Workflows & CI/CD

Follow this real-world step-by-step lab to practice Git commands, push code to your GitHub account, open a Pull Request, watch GitHub Actions execute automated tests, and cut an official release tag.

---

## Lab Prerequisites
1. Open terminal and navigate to this project:
   ```bash
   cd c:\Users\2869026\Desktop\visual\git-cicd-retail-hub
   ```
2. Confirm unit tests pass locally:
   ```bash
   python -m unittest discover -s tests -v
   ```
   *(You should see 14 tests passing with `OK`)*

---

## Step 1: Create Your New Repository on GitHub
1. Open your web browser and sign in to **[GitHub.com](https://github.com)**.
2. In the top-right corner, click **`+`** -> **New repository**.
3. Fill in the repository details:
   - **Repository name**: `retail-pricing-engine` (or any name you prefer)
   - **Visibility**: `Public` (recommended for free unlimited GitHub Actions runners) or `Private`
   - **Initialize this repository with**:
     - ⚠️ **DO NOT check** "Add a README file"
     - ⚠️ **DO NOT check** "Add .gitignore"
     - ⚠️ **DO NOT check** "Choose a license"
     *(Leaving these unchecked ensures your remote repository starts empty, matching your local repository)*
4. Click **Create repository**.
5. GitHub will display a page with your new repository URL:
   `https://github.com/<your-username>/retail-pricing-engine.git`

---

## Step 2: Link Your Local Project to GitHub
In your local terminal inside `git-cicd-retail-hub`:

```bash
# 1. Switch to the main branch
git switch main

# 2. Add the remote GitHub repository link (replace with your actual GitHub URL)
git remote add origin https://github.com/<your-username>/retail-pricing-engine.git

# 3. Verify the remote is set correctly
git remote -v
```

---

## Step 3: Push Your Code to GitHub
Upload your commits to GitHub and configure upstream branch tracking:

```bash
# Push the main branch to GitHub (-u sets upstream tracking)
git push -u origin main
```
*(If prompted by Git Credential Manager, sign in with your GitHub account in the browser or personal access token)*.

---

## Step 4: Watch Your First CI/CD Pipeline Run Live!
1. Open your repository on **GitHub.com**.
2. Click on the **"Actions"** tab at the top.
3. You will see a workflow running named **`Retail Hub CI/CD Pipeline`**!
4. Click on the run to view the execution live:
   - **Job 1 (Lint)**: Checks code formatting and syntax with `flake8`.
   - **Job 2 (Test Matrix)**: Spawns **3 parallel virtual machines** running your unit tests across Python 3.10, 3.11, and 3.12!
5. All green checkmarks indicate your code is production-healthy.

---

## Step 5: Practice Feature Branching
In professional teams, developers never push directly to `main`. Let's create an isolated feature branch to add Georgia state sales tax (`GA: 0.0400`):

```bash
# Create and switch to a new feature branch
git switch -c feature/add-georgia-tax

# Verify you are on the new branch
git branch
```

---

## Step 6: Make Code Changes & Test
1. Open `src/retail_calc.py` and add `"GA": 0.0400` to `tax_rates`:
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
2. Open `tests/test_retail_calc.py` and add a test:
   ```python
   def test_sales_tax_ga(self):
       tax = calculate_sales_tax(100.00, "GA")
       self.assertEqual(tax, 4.00)
   ```
3. Run tests locally to ensure they pass:
   ```bash
   python -m unittest discover -s tests -v
   ```

---

## Step 7: Inspect Diffs, Stage & Commit

```bash
# 1. Inspect what you changed
git diff

# 2. Stage the modified files
git add src/retail_calc.py tests/test_retail_calc.py

# 3. Check staging area status
git status

# 4. Commit with conventional commit message
git commit -m "feat: add Georgia state sales tax rate calculation"
```

---

## Step 8: Push Feature Branch to GitHub

```bash
git push -u origin feature/add-georgia-tax
```

---

## Step 9: Open and Merge a Pull Request (PR)
1. Go to your repository on **GitHub.com**.
2. You will see a banner: **`feature/add-georgia-tax had recent pushes`** with a green button: **"Compare & pull request"**. Click it.
3. Review your title and description, then click **"Create pull request"**.
4. Notice how GitHub Actions automatically triggers and runs all linting and test matrix checks on your Pull Request!
5. Once checks turn green (Passing), click **"Merge pull request"** -> **"Confirm merge"**.
6. Click **"Delete branch"** on GitHub to keep your repository tidy.

---

## Step 10: Sync Your Local Main Branch

Now that the Pull Request was merged on GitHub, sync your local machine:

```bash
# 1. Switch back to main
git switch main

# 2. Pull the newly merged commits from GitHub
git pull origin main

# 3. Delete the local feature branch
git branch -d feature/add-georgia-tax

# 4. View your commit tree
git log --oneline --graph
```

---

## Step 11: Cut an Official Release Version Tag (CI/CD Deployment)

Release tags mark stable software versions (e.g. `v1.0.0`, `v1.1.0`). Pushing a tag automatically triggers the **Build & Package** step in GitHub Actions:

```bash
# 1. Create an annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Enterprise Retail Pricing Microservice"

# 2. Push the tag to GitHub
git push origin v1.0.0
```

1. Open the **Actions** tab on GitHub.
2. You will see Job 3 (**Build & Package Artifacts**) execute!
3. When finished, you will find downloadable package distribution wheels (`.whl` and `.tar.gz`) attached to the GitHub run under **Artifacts**!

---

## Step 12: Roadmap Preview — Docker Containers & Azure Deployment
When you are ready to transition to Docker containerization and cloud deployment:
1. **Local Docker Run**:
   ```bash
   docker build -t retail-pricing-engine .
   docker run -d -p 8000:8000 retail-pricing-engine
   ```
2. **Access Swagger UI**: `http://localhost:8000/docs`
3. **Azure Cloud Deployment**:
   - Push image to Azure Container Registry (ACR): `acrexploreai65064.azurecr.io`
   - Deploy as serverless container in Azure Container Apps (ACA) or Azure Kubernetes Service (AKS).
