# Retail Hub Pricing & Checkout Engine

![CI/CD Pipeline](https://github.com/USER/git-cicd-retail-hub/actions/workflows/ci-cd.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A modular, test-driven Python calculation microservice demonstrating production Git workflows, branching models, and GitHub Actions CI/CD automation.

## Features
- **Cart Subtotal Calculation**: Aggregates line item quantities and unit prices.
- **Promotional Coupons**: Supports `WELCOME10` (10%), `VIP20` (20%), `FLASH50` (50%).
- **Multi-State Sales Tax**: Automatic rate calculations for TX, CA, NY, IL, and FL.
- **Automated CI/CD**: Flake8 linting and multi-version Python matrix testing (`3.10`, `3.11`, `3.12`) via GitHub Actions.

## Quick Start
```bash
# Run tests locally
python -m unittest discover -s tests -v
```
