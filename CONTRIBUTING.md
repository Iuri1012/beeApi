# Contributing to BeeAPI

Thank you for your interest in contributing to BeeAPI! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/beeApi.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Using Docker (Recommended)

```bash
./scripts/run_local.sh
```

### Local Development

```bash
# See all options
./scripts/dev.sh

# Run individual components
./scripts/dev.sh backend
./scripts/dev.sh telemetry
./scripts/dev.sh web
./scripts/dev.sh simulator
```

## Project Structure

```
beeApi/
├── firmware/          # Device firmware and simulator
├── gateway/           # IoT gateway (future)
├── backend/           # FastAPI REST API
├── telemetry/         # MQTT telemetry consumer
├── timeseries/        # TimescaleDB schemas
├── web/               # React dashboard
├── docs/              # Documentation
├── docker/            # Docker configurations
├── scripts/           # Utility scripts
└── .github/           # GitHub templates and workflows
```

## Code Style

### Python
- Follow PEP 8
- Use type hints where appropriate
- Use Black for formatting: `black .`
- Use flake8 for linting: `flake8 . --max-line-length=120`

### JavaScript/React
- Follow Airbnb style guide
- Use ESLint
- Use Prettier for formatting

### SQL
- Use uppercase for SQL keywords
- Use snake_case for table and column names
- Include comments for complex queries

## Testing

### Run all tests
```bash
python3 scripts/test_integration.py
```

### Validate structure
```bash
./scripts/validate_structure.sh
```

### Component-specific tests

#### Backend
```bash
cd backend
pytest
```

#### Web
```bash
cd web
npm test
```

## Making Changes

### Adding a New Feature

1. Create an issue describing the feature
2. Create a feature branch from `main`
3. Implement the feature with tests
4. Update documentation
5. Submit a pull request

### Fixing a Bug

1. Create an issue describing the bug
2. Create a bugfix branch from `main`
3. Fix the bug with tests
4. Submit a pull request

### Updating Documentation

Documentation updates are always welcome!

- API documentation: `docs/API.md`
- Architecture: `docs/README.md`
- Testing guide: `docs/TESTING.md`

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation in `docs/` as appropriate
3. Ensure all tests pass
4. Request review from maintainers
5. Address review feedback

## Code Review Guidelines

When reviewing code:
- Be respectful and constructive
- Focus on code quality and maintainability
- Check for security issues
- Verify tests are included
- Ensure documentation is updated

## Commit Messages

Follow conventional commits format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(backend): add device health endpoint

Add new endpoint to check device health status
Returns last seen timestamp and connection status

Closes #123
```

```
fix(telemetry): handle missing timestamp in MQTT payload

Use current time if timestamp is not provided in payload
Prevents database errors

Fixes #124
```

## Reporting Bugs

Use the bug report template when creating an issue:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details

## Feature Requests

Use the feature request template:
- Clear description of the feature
- Use case / motivation
- Proposed solution
- Alternatives considered

## Community Guidelines

- Be respectful and inclusive
- Help newcomers
- Share knowledge
- Follow code of conduct

## Questions?

- Open a discussion in GitHub Discussions
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
