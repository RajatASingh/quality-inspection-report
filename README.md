# OM Industries Process Sheet

This app creates a process sheet for OM Industries.

## What it does

- Enter process sheet details.
- Download the process sheet as a PDF file.
- Use the last text values again the next time you fill the form.

## Setup

Open a terminal in this folder.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run demo.py
```

The app will open in your web browser.

## Use the app

1. Fill in the process sheet.
2. Click **Generate PDF**.
3. Click **Download Process Sheet PDF**.

The app saves the text values when you generate a PDF. These values appear in the fields the next time you open the app. Dates are not saved as suggestions.

## Stop the app

Press `Ctrl+C` in the terminal.
