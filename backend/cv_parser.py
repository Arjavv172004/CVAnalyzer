import pdfplumber
import re

def extract_cv_data(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
    except:
        pass

    if not text.strip():
        print(f"❌ No extractable text in: {path}")

    email = re.search(r'[\w\.-]+@[\w\.-]+', text)

    return {
        'name': path.split('/')[-1].replace('.pdf', ''),
        'email': email.group(0) if email else 'noemail@example.com',
        'text': text
    }
