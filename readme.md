# Docx Summarizer Web App

This is a lightweight Flask web application that allows users to upload `.docx` files and receive a summary of their contents. The app uses NLTK for sentence tokenization and stopword removal, and it supports summarization via frequency-based scoring.

## Features

- Upload `.docx` files via a web interface
- Extract and summarize key insights from uploaded documents
- View summaries in a clean HTML format
- Logging support for debugging and tracking activity

## Summary Algorithms

The default implementation uses a simple frequency-based sentence scoring method. You can optionally switch to using `TextRank`, `Luhn`, or `LSA` summarizers from the `sumy` library.

## Tech Stack

- **Flask** – Web framework
- **NLTK** – Natural language processing (tokenization, stopwords)
- **Sumy** – Text summarization algorithms
- **python-docx** – Extracting text from `.docx` files
- **HTML/Jinja2** – Front-end templates for upload form

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/docx-summarizer.git
   cd docx-summarizer
