# CI/CD Setup Guide

This guide covers setting up Codecov and configuring branch protection for the Mantis Bot project.

## Codecov Setup

### Step 1: Sign up for Codecov

1. Go to [https://codecov.io](https://codecov.io)
2. Click "Sign Up" and sign in with your GitHub account
3. Authorize Codecov to access your GitHub repositories

### Step 2: Add the Repository

1. After signing in, click "Add New Repository"
2. Find and select `mantis` (or your repository name)
3. Click "Setup" to get your upload token

### Step 3: Add Codecov Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click "New repository secret"
4. Name: `CODECOV_TOKEN`
5. Value: Paste the token from Codecov (looks like a long UUID)
6. Click "Add secret"

### Step 4: Update README.md Badges

Replace `YOUR_USERNAME` in the README.md badges with your actual GitHub username:

```markdown
[![CI](https://github.com/YOUR_USERNAME/mantis/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/mantis/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/mantis/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/mantis)
```

## Branch Protection Setup

### Step 1: Access Repository Settings

1. Go to your GitHub repository
2. Click **Settings → Branches**

### Step 2: Add Branch Protection Rule

1. Click "Add rule" or "Edit" if `main` already exists
2. Branch name pattern: `main`

### Step 3: Configure Required Status Checks

Under "Protect matching branches", enable:
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals** (optional - set number of reviewers)
  - ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**

### Step 4: Select Required Checks

Search for and select these status checks:
- ✅ `Lint Backend (Ruff)`
- ✅ `Lint Frontend (ESLint/Prettier/TypeScript)`
- ✅ `Test Backend (pytest)`
- ✅ `Test Frontend (Jest)`

**Note:** Do NOT select `E2E Tests (Playwright)` as it's marked optional with `continue-on-error: true`.

### Step 5: Additional Restrictions (Optional)

- ✅ **Require signed commits** (if using GPG signing)
- ✅ **Require linear history** (prevents merge commits, requires rebase)
- ✅ **Include administrators** (enforces rules on repo admins too)

### Step 6: Save Changes

Click "Create" or "Save changes" to apply the branch protection rule.

## Verification

### Test the CI Pipeline

To verify everything works:

1. Create a new branch:
   ```bash
   git checkout -b test-ci-pipeline
   ```

2. Make a small change (e.g., update README.md):
   ```bash
   echo "# Testing CI Pipeline" >> README.md
   ```

3. Commit and push:
   ```bash
   git add README.md
   git commit -m "test: verify CI pipeline"
   git push origin test-ci-pipeline
   ```

4. Create a pull request on GitHub

5. Verify all status checks pass:
   - Lint Backend (Ruff) ✅
   - Lint Frontend (ESLint/Prettier/TypeScript) ✅
   - Test Backend (pytest) ✅
   - Test Frontend (Jest) ✅

6. Check coverage reports on Codecov

### Troubleshooting

**Codecov upload fails:**
- Verify `CODECOV_TOKEN` is set correctly in repository secrets
- Check the token hasn't expired or been revoked

**Tests fail in CI but pass locally:**
- Check environment variables match between local and CI
- Ensure database services are healthy before tests run
- Review CI logs for specific error messages

**Branch protection blocks merge:**
- Ensure all required status checks have passed
- Check that branch is up to date with main branch
- Verify you have sufficient permissions to merge

## Summary

After completing these steps:

✅ CI pipeline runs on every pull request and push
✅ Code quality enforced via linting and testing
✅ Coverage reports uploaded to Codecov
✅ Branch protection prevents merging without CI pass
✅ Status badges show current build status in README

The repository is now ready for team development with automated quality gates!
