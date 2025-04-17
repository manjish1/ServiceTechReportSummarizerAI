{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Docx Summarizer Web App\
\
This is a lightweight Flask web application that allows users to upload `.docx` files and receive a summary of their contents. The app uses NLTK for sentence tokenization and stopword removal, and it supports summarization via frequency-based scoring.\
\
## Features\
\
- Upload `.docx` files via a web interface\
- Extract and summarize key insights from uploaded documents\
- View summaries in a clean HTML format\
- Logging support for debugging and tracking activity\
\
## Summary Algorithms\
\
The default implementation uses a simple frequency-based sentence scoring method. You can optionally switch to using `TextRank`, `Luhn`, or `LSA` summarizers from the `sumy` library.\
\
## Tech Stack\
\
- **Flask** \'96 Web framework\
- **NLTK** \'96 Natural language processing (tokenization, stopwords)\
- **Sumy** \'96 Text summarization algorithms\
- **python-docx** \'96 Extracting text from `.docx` files\
- **HTML/Jinja2** \'96 Front-end templates for upload form\
\
## Setup Instructions\
\
1. **Clone the repository**:\
\
   ```bash\
   git clone https://github.com/yourusername/docx-summarizer.git\
   cd docx-summarizer\
}