# M&A Value Creation Code Repository

This repository contains the code, data, and statistical analysis pipeline for the master's thesis titled:

**"Value Creation in European Health Care M&A"**

Written by:

**Bendtsen & Urholt (2025)**

Studying MSc in Applied Economics and Finance at Copenhagen Business School.

# Overview

This study investigates whether mergers and acquisitions (M&As) involving Western European acquirers in the Health Care sector generate short-term value creation for shareholders. The empirical analysis employs:

- Event Study Methodology (MacKinlay, 1997)
- Fama-French Three-Factor Model for estimating expected returns
- Cross-sectional regressions to examine how deal-, firm-, and market-specific variables influence cumulative abnormal returns (CARs)

The empirical implementation and data engineering are conducted primarily in Python, with auxiliary scripts in R and VBA.

## Repository Structure

MA/
├── Capital IQ & Yahoo Finance Data Cleaning/   # Data fetching, data treatment, abnormal return calculation and final sample construction
├── data/                                       # Contains final sample files and cleaned datasets that are used for analyses
├── Descriptive Statistics/                     # Scripts for summary statistics, distribution plots, and CAR diagnostics
├── multivariate/                               # Cross-sectional regression models and sensitivity tests
├── .gitignore
└── README.md

