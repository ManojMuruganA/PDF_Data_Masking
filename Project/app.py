from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import fitz
import re
import os
import langid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

name_pattern = re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b')
phone_pattern = re.compile(r'\b\+?\d{1,4}[\s-]?\(?\d+\)?[\s-]?\d+[\s-]?\d+\b')
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
clinic_pattern = re.compile(r'\b[A-Z][a-z]+ Clinic\b')
chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
malaysian_name_pattern = re.compile(r'\b[A-Z][a-z]+\sbin\s[A-Z][a-z]+\b|\b[A-Z][a-z]+\sbinti\s[A-Z][a-z]+\b')
korean_name_pattern = re.compile(r'[\uac00-\ud7a3]+')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def mask_sensitive_text(text):
    """ Mask detected sensitive information in the text. """
    text = name_pattern.sub(lambda x: '*' * len(x.group()), text)
    text = phone_pattern.sub(lambda x: '*' * len(x.group()), text)
    text = email_pattern.sub(lambda x: '*' * len(x.group()), text)
    text = clinic_pattern.sub(lambda x: '*' * len(x.group()), text)
    text = chinese_pattern.sub(lambda x: '*' * len(x.group()), text)
    text = malaysian_name_pattern.sub(lambda x: '*' * len(x.group()), text)
    text = korean_name_pattern.sub(lambda x: '*' * len(x.group()), text)
    return text

def detect_language(text):
    """ Detect the language of the text. """
    try:
        lang, _ = langid.classify(text)
        return lang
    except:
        return "unknown"

def mask_pdf(file_path):
    doc = fitz.open(file_path)
    for page in doc:
        spans = []
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for l in b["lines"]:
                for s in l["spans"]:
                    original_text = s["text"]
                    language = detect_language(original_text)
                    masked_text = mask_sensitive_text(original_text)
                    if masked_text != original_text:
                        r = fitz.Rect(s["bbox"])
                        page.add_redact_annot(r)
                        spans.append((r, s, masked_text))
        page.apply_redactions()

        for r, s, nword in spans:
            fsize = s["size"]
            flags = s["flags"]
            if flags & 2*1 & 2*4:
                fname = "hebi"
            elif flags & 2**1:
                fname = "heit"
            elif flags & 2**4:
                fname = "hebo"
            else:
                fname = "helv"
            origin = s["origin"]
            page.insert_text(origin, nword, fontsize=fsize, fontname=fname)

    output_file = file_path.replace(".pdf", "-redacted.pdf")
    doc.save(output_file)
    return output_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        redacted_file = mask_pdf(file_path)
        return redirect(url_for('download_file', filename=os.path.basename(redacted_file)))
    return redirect(request.url)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)