# DevTools

A collection of development tools, scripts, and utilities for setting up and maintaining development environments.

## Overview

This project provides a set of tools to automate the installation and configuration of development tools, system analysis, and AI-assisted research capabilities. It's designed to work on Ubuntu/Debian-based systems and includes both shell scripts and Python utilities.

## Components

### Installation Tools

- **install-tools.sh**: Automated script to install and configure development tools including:
  - GitHub CLI with authentication
  - Tabby terminal emulator
  - Wave terminal
  - Python virtual environment with development dependencies
  - Flatpak support for GUI applications

### AI Research Tools

- **perplexity_client.py**: Python client for automating queries to Perplexity AI
  - Uses Selenium for web automation
  - Supports both English and Estonian queries
  - Includes logging and response storage
  - Works in offline mode with mock responses when needed

### System Analysis

- **scripts/analyze-system.sh**: Comprehensive system analysis script that:
  - Identifies failed services
  - Logs kernel and boot messages
  - Checks for file system errors
  - Identifies broken packages
  - Monitors crontab errors
  - Reviews system and authentication logs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/devtools.git
   cd devtools
   ```

2. Run the installation script:
   ```bash
   ./install-tools.sh
   ```

3. Set up environment variables (create .env file based on the template):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Usage

### Installing Development Tools

```bash
./install-tools.sh
```

The script will:
- Add GitHub CLI repository and install it
- Set up GitHub authentication
- Install Tabby terminal (AMD64)
- Install Wave Terminal
- Configure Python virtual environment with development dependencies
- Set up Flatpak support for GUI applications

### Using Perplexity AI Client

```python
from perplexity_client import PerplexityClient

# Initialize client
client = PerplexityClient(data_dir="data")

try:
    # Query in English
    response = client.query_perplexity("What is the capital of Estonia?")
    print(response.json(indent=2))
    
    # Query in Estonian
    response = client.query_perplexity("Mis on Eesti pealinn?")
    print(response.json(indent=2))
finally:
    client.close()
```

Responses are automatically logged to the `data` directory as JSON files.

### Running System Analysis

```bash
./scripts/analyze-system.sh
```

This will generate a comprehensive system report and save it to `~/system_analysis_YYYYMMDD_HHMMSS.log`.

## Development Setup

1. Set up a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install development dependencies:
   ```bash
   pip install selenium webdriver-manager pydantic
   ```

3. Run tests:
   ```bash
   # TODO: Add test commands
   ```

---

# DevTools (Eesti keeles)

Arendustööriistade, skriptide ja utiliitide kogu arenduskeskkondade seadistamiseks ja hooldamiseks.

## Ülevaade

See projekt pakub komplekti tööriistu arendustööriistade installimise ja konfigureerimise, süsteemianalüüsi ning AI-toega uurimisfunktsioonide automatiseerimiseks. See on mõeldud töötama Ubuntu/Debian-põhistel süsteemidel ning sisaldab nii shell-skripte kui ka Python-utiliite.

## Komponendid

### Paigaldustööriistad

- **install-tools.sh**: Automatiseeritud skript arendustööriistade installimiseks ja konfigureerimiseks, sealhulgas:
  - GitHub CLI koos autentimisega
  - Tabby terminaliemulaator
  - Wave terminal
  - Python virtuaalkeskkond arendussõltuvustega
  - Flatpak tugi GUI rakendustele

### AI Uurimistööriistad

- **perplexity_client.py**: Python-klient Perplexity AI päringute automatiseerimiseks
  - Kasutab Seleniumi veebiautomaatika jaoks
  - Toetab nii inglise kui ka eesti keelseid päringuid
  - Sisaldab logimist ja vastuste salvestamist
  - Töötab offline-režiimis mock-vastustega, kui vaja

### Süsteemianalüüs

- **scripts/analyze-system.sh**: Põhjalik süsteemianalüüsi skript, mis:
  - Tuvastab nurjunud teenuseid
  - Logib kerneli ja alglaadimise teateid
  - Kontrollib failisüsteemi vigu
  - Tuvastab katkiseid pakette
  - Jälgib crontab vigu
  - Vaatab üle süsteemi- ja autentimislogid

## Paigaldamine

1. Klooni repositoorium:
   ```bash
   git clone https://github.com/yourusername/devtools.git
   cd devtools
   ```

2. Käivita paigaldusskript:
   ```bash
   ./install-tools.sh
   ```

3. Seadista keskkonnamuutujad (loo .env fail malli põhjal):
   ```bash
   cp .env.example .env
   # Muuda .env faili seadistusi
   ```

## Kasutamine

### Arendustööriistade paigaldamine

```bash
./install-tools.sh
```

Skript:
- Lisab GitHub CLI repositooriumi ja installib selle
- Seadistab GitHub-i autentimise
- Installib Tabby terminali (AMD64)
- Installib Wave terminali
- Konfigureerib Python virtuaalkeskkonna arendussõltuvustega
- Seadistab Flatpak toe GUI rakendustele

### Perplexity AI kliendi kasutamine

```python
from perplexity_client import PerplexityClient

# Initsialiseerime kliendi
client = PerplexityClient(data_dir="data")

try:
    # Päring inglise keeles
    response = client.query_perplexity("What is the capital of Estonia?")
    print(response.json(indent=2))
    
    # Päring eesti keeles
    response = client.query_perplexity("Mis on Eesti pealinn?")
    print(response.json(indent=2))
finally:
    client.close()
```

Vastused logitakse automaatselt `data` kausta JSON-failidena.

### Süsteemianalüüsi käivitamine

```bash
./scripts/analyze-system.sh
```

See genereerib põhjaliku süsteemiaruande ja salvestab selle faili `~/system_analysis_YYYYMMDD_HHMMSS.log`.

## Arenduse seadistamine

1. Seadista Python virtuaalkeskkond:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Installi arendussõltuvused:
   ```bash
   pip install selenium webdriver-manager pydantic
   ```

3. Käivita testid:
   ```bash
   # TODO: Lisa käsud testide käivitamiseks
   ```

