# Git Repository Setup Guide

This repository doesn't have a remote configured yet. Follow these steps to set up the remote repository and trigger the CI pipeline.

## Step 1: Create GitHub Repository

1. Go to [https://github.com/new](https://github.com/new)
2. Create a new repository named `mantis` (or your preferred name)
3. **Important:** Do NOT initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

## Step 2: Add Remote Repository

After creating the repository, GitHub will show you the setup commands. Run:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/mantis.git

# Or use SSH if you have SSH keys configured:
# git remote add origin git@github.com:YOUR_USERNAME/mantis.git

# Verify the remote was added
git remote -v
```

## Step 3: Push the Test Branch

Now push the test branch to trigger the CI pipeline:

```bash
# Push the test branch
git push -u origin test-ci-pipeline
```

## Step 4: Verify CI Pipeline

1. Go to your GitHub repository
2. You should see a yellow/orange dot indicating the CI workflow is running
3. Click the "Actions" tab to see the workflow execution
4. Verify all jobs pass:
   - ✅ Lint Backend (Ruff)
   - ✅ Lint Frontend (ESLint/Prettier/TypeScript)
   - ✅ Test Backend (pytest)
   - ✅ Test Frontend (Jest)
   - ⚠️ E2E Tests (Playwright) - May fail or skip (optional)

## Step 5: Merge to Main (After CI Passes)

Once all required checks pass:

1. Create a pull request from `test-ci-pipeline` to `main`
2. Verify all status checks are green
3. Merge the pull request
4. Delete the `test-ci-pipeline` branch

## Alternative: Push to Main Directly

If you don't want to create a pull request, you can push directly to main (after testing):

```bash
# Switch back to main branch
git checkout main

# Merge the test branch
git merge test-ci-pipeline

# Push to main (this will trigger CI)
git push -u origin main

# Delete the test branch locally
git branch -d test-ci-pipeline
```

## Next Steps After Remote is Set Up

Once the repository is pushed to GitHub:

1. **Set up Codecov** - Follow the instructions in `docs/CI_SETUP.md`
2. **Configure branch protection** - Follow the instructions in `docs/CI_SETUP.md`
3. **Update README badges** - Replace `YOUR_USERNAME` with your actual GitHub username

## Quick Start Commands

```bash
# Example commands (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/mantis.git
git push -u origin test-ci-pipeline

# After CI passes, create PR via GitHub UI or:
gh pr create --title "feat: implement CI/CD pipeline" --body "Testing CI pipeline implementation"
```

## Troubleshooting

**"Permission denied" error:**
- Make sure you have push access to the repository
- If using HTTPS, you may need to use a personal access token instead of password
- Consider using SSH instead: `git remote set-url origin git@github.com:YOUR_USERNAME/mantis.git`

**"Repository not found" error:**
- Verify the repository URL is correct
- Make sure the repository exists on GitHub
- Check that you have the correct permissions
