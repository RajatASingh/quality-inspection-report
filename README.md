# Quality Rejection Report

This app creates a quality rejection report.

## What it does

- Enter report details.
- Add the reason for rejection.
- Upload one or more photos.
- Add the corrective action.
- Download the report as a Word file or a PDF file.

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
streamlit run create_word.py
```

The app will open in your web browser.

## Use the app

1. Fill in the report details.
2. Enter the reason for rejection.
3. Upload one or more photos.
4. Enter the corrective action and date.
5. Click **SUBMIT REJECTION REPORT**.
6. Click **Download Word Report** or **Download PDF Report**.

## Stop the app

Press `Ctrl+C` in the terminal.
