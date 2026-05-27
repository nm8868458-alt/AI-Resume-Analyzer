from flask import Flask, render_template, request, jsonify
import os
from parser_utils import extract_text
from gemini_utils import analyze_resume_with_gemini
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html', error=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return render_template('index.html', error="No file uploaded. Please upload a valid resume.")
        
    file = request.files['resume']
    if file.filename == '':
        return render_template('index.html', error="No file selected. Please select a resume file.")

    api_key = request.form.get('api_key') or os.getenv("GEMINI_API_KEY")

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract text
        resume_text = extract_text(filepath)
        
        if not resume_text:
            return render_template(
                'index.html', 
                error="Could not extract text. This usually happens if the PDF is a scanned image/photo. Please upload a digitally generated PDF or a DOCX file."
            )

        # AI Analysis
        analysis_results = analyze_resume_with_gemini(resume_text, api_key)

        return render_template(
            'result.html',
            results=analysis_results,
            filename=file.filename
        )

if __name__ == '__main__':
    app.run(debug=True, port=5000)