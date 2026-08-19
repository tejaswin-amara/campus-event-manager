# 🤝 Contributing to CampusConnect

Thank you for your interest in contributing to **CampusConnect**! We value the participation of our student community and contributors in making this a world-class campus event management ecosystem.

---

## 🧭 How to Get Started

Before you start contributing, please ensure you have:
1. **Searched the [Issue Tracker](../../issues)** to check if the bug or feature request has already been reported.
2. **Read the [TECHNICAL_GUIDE.md](./TECHNICAL_GUIDE.md)** to understand the project architecture and development workflow.

---

## 🛠️ Development Workflow

### 1. Fork and Clone
Fork the repository and clone it to your local machine:
```bash
git clone https://github.com/tejaswin-amara/campus-connect.git
cd campus-connect
```

### 2. Create a Topic Branch
Always develop your features or fixes in a separate branch:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Setup and Testing
Ensure your environment is set up according to the [README.md](./README.md). Before making changes, verify that the existing test suite passes:
```bash
./mvnw clean test
```

### 4. Code Standards & Style
- Follow standard Java coding conventions.
- Maintain a **mobile-first** approach for any UI changes.
- Ensure all new logic is covered by unit tests.

---

## 📤 Submitting Changes

### Open a Pull Request
Once you are finished with your changes:
1. Push your branch to GitHub.
2. Open a Pull Request (PR) against the `main` branch.
3. Use the provided **Pull Request Template** to describe your changes.
4. Ensure the **GitHub Actions CI** build passes for your PR.

> **Note:** Link your PR to a specific issue using keywords like `Closes #123` or `Fixes #456` in the description.

---

## ⚖️ Code of Conduct
By participating in this project, you agree to abide by our community standards and treat all contributors with respect and professionalism.

Thank you for making **CampusConnect** better for everyone! ❤️

## Commit and review conventions

Use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format for commit subjects, such as `feat: add event capacity validation`, `fix: prevent duplicate interests`, `docs: map CO1 evidence`, or `ci: publish coverage artifact`. Keep commits focused so reviewers can distinguish behavior changes, operational changes, and documentation changes.

Pull requests should explain the user or operational problem, identify database and security impact, link the relevant requirement or issue, and include test evidence. Reviewers should verify migration safety, authorization boundaries, validation behavior, error handling, observability, rollback considerations, and documentation accuracy. The review checklist is informed by the supplied [Google Engineering Practices](https://github.com/google/eng-practices) and [GitHub Open Source Guide](https://github.com/github/opensource.guide).

Before opening a pull request, run:

```bash
./mvnw -B verify
BASE_URL=http://localhost:9090 ./scripts/smoke-test.sh
REQUESTS=100 CONCURRENCY=10 BASE_URL=http://localhost:9090 ./scripts/load-test.sh
```

Never commit `.env`, passwords, private keys, generated uploads, or production database URLs. Use `.env.example` for placeholders and repository/environment secrets for actual deployments.
