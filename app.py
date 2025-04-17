from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import docx
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# Explicitly set NLTK data path
nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))
nltk.download('punkt_tab', download_dir=os.path.join(os.getcwd(), "nltk_data"))
nltk.download('punkt', download_dir=os.path.join(os.getcwd(), "nltk_data"))
nltk.download('stopwords', download_dir=os.path.join(os.getcwd(), "nltk_data"))
nltk.download('punkt', download_dir=os.path.join(os.getcwd(), "nltk_data"))

print(nltk.data.path)

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Checks if the file is allowed based on its extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(file_path):
    """Extracts text from a .docx file"""
    try:
        doc = docx.Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        logger.debug(f"Extracted text from {file_path}")
        return full_text
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        raise

def summarize_text(text, num_sentences=5, algorithm="textrank"):
    """Summarizes the extracted text by focusing on key insights."""
    try:
        # 1. Tokenize the text into sentences
        sentences = sent_tokenize(text)

        # 2. Remove stop words and punctuation
        stop_words = set(stopwords.words('english'))
        words = [word.lower() for sentence in sentences for word in nltk.word_tokenize(sentence) if word.isalnum() and word.lower() not in stop_words]

        # 3. Calculate word frequency
        word_frequency = {}
        for word in words:
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1

        # 4. Score sentences based on word frequency
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_frequency:
                    if len(sentence.split(" ")) < 30:  # Consider only sentences with a reasonable length
                        if i in sentence_scores:
                            sentence_scores[i] += word_frequency[word]
                        else:
                            sentence_scores[i] = word_frequency[word]

        # 5. Get the top N sentences as key insights
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        key_insights = [sentences[i] for i in top_sentences]

        logger.debug("Summarization complete")
        return key_insights

    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        raise

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "files" not in request.files:
            logger.warning("No file part in request")
            return "No file part"

        files = request.files.getlist("files")
        summaries = {}

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Log the file before attempting to save
                logger.debug(f"Processing file: {filename}")

                try:
                    # Save the file to the upload folder
                    file.save(file_path)
                    logger.info(f"File saved to {file_path}")

                    # Process file
                    text = extract_text_from_docx(file_path)
                    key_insights = summarize_text(text, algorithm="textrank")

                    # Format the output as a bulleted list
                    formatted_insights = "<ul>\n"
                    for insight in key_insights:
                        formatted_insights += f"  <li>{insight}</li>\n"
                    formatted_insights += "</ul>"
                    summaries[filename] = formatted_insights
                    logger.info(f"Summary for {filename} created")

                except Exception as e:
                    logger.error(f"Error processing file {filename}: {e}")
                    summaries[filename] = f"Error processing file: {e}"

        return jsonify(summaries)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)