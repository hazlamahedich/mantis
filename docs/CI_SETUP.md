# CI/CD Setup Guide

This guide covers setting up Codecov and configuring branch protection for the Mantis Bot project.

## ✅ Codecov Setup (Already Configured)

The Codecov token has been added to GitHub Secrets:
- Secret Name: `CODECOV_TOKEN`
- Status: ✅ Active
- Repository visibility: ✅ **PUBLIC** (enables full Codecov features)

Coverage reports will be automatically uploaded to Codecov on every CI run.

### Manual Setup (Reference Only)

If you need to reconfigure Codecov in the future:

1. Go to [https://codecov.io](https://codecov.io)
2. Sign in with your GitHub account
3. Add the `mantis` repository
4. Get the upload token from repository settings
5. Add to GitHub: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `CODECOV_TOKEN`
   - Value: Paste the token from Codecov

## ✅ Branch Protection Setup (Ready to Configure)

**Repository Status:** PUBLIC - Branch protection rules are now available!

The repository has been made public, which enables:
- Branch protection rules (even on free GitHub accounts)
- Full Codecov integration without tokenless upload limitations
- Better community visibility and collaboration

### Manual Branch Protection Configuration

Since the GitHub API configuration is complex, follow these manual steps to configure branch protection:

1. **Go to repository settings**:
   - Navigate to https://github.com/hazlamahedich/mantis/settings/branches

2. **Add branch protection rule**:
   - Click **Add rule**
   - Branch name pattern: `master`

3. **Configure protection settings**:
   - ✅ **Require status checks to pass before merging**
     - Uncheck "Require branches to be up to date before merging" (optional)
     - Search and add these required checks:
       - `Lint Backend (Ruff)`
       - `Lint Frontend`
       - `Test Backend`
       - `Test Frontend`

4. **Optional settings**:
   - ✅ **Require pull request before merging** (recommended)
   - ✅ **Require conversation resolution** (recommended)
   - ❌ Do NOT require approvals (unless desired)
   - ✅ **Include administrators** (recommended to enforce rules on admins too)

5. **Click Create** to apply the rule

### Verification

To verify branch protection is working:
1. Create a test branch: `git checkout -b test-branch-protection`
2. Make a small change: `echo "test" >> README.md`
3. Commit and push: `git add README.md && git commit -m "test" && git push origin test-branch-protection`
4. Create a pull request on GitHub
5. Verify all 4 status checks are required before merging

### Step 4: Update README.md Badges

Replace `YOUR_USERNAME` in the README.md badges with your actual GitHub username:

```markdown
[![CI](https://github.com/YOUR_USERNAME/mantis/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/mantis/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/mantis/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/mantis)
```

## Branch Protection Setup

**⚠️ Important**: Branch protection rules require **GitHub Pro/Team** for private repositories or a **public repository**. Free GitHub accounts cannot configure branch protection on private repos.

### For Free GitHub Accounts (Private Repository)

You have two options:

**Option 1 - Make repository public:**
1. Go to **Settings → General → Danger Zone**
2. Click **Change visibility** → Make public
3. Then follow the branch protection steps below

**Option 2 - Manual status check verification:**
1. Always create pull requests for changes
2. Wait for all CI checks to pass (green checkmarks)
3. Review the code changes thoroughly
4. Merge only when all 4 checks pass:
   - ✅ Lint Backend (Ruff)
   - ✅ Lint Frontend
   - ✅ Test Backend
   - ✅ Test Frontend

### For GitHub Pro/Team or Public Repositories

1. Go to your GitHub repository
2. Click **Settings → Branches**
3. Click "Add rule"
4. Branch name pattern: `master` (or `main`)
5. Configure:
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
6. Select these required checks:
   - ✅ `Lint Backend (Ruff)`
   - ✅ `Lint Frontend`
   - ✅ `Test Backend`
   - ✅ `Test Frontend`
7. Click "Create"

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
