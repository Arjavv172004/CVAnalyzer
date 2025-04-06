from database import init_db
from flask import Flask, request, jsonify
from flask_cors import CORS
from jd_parser import get_all_jobs, summarize_jd
from cv_parser import extract_cv_data
from matcher import match_score
from mailer import send_mail
import os

app = Flask(__name__)
CORS(app)

CV_FOLDER = '../CV'
MATCH_THRESHOLD = 80

@app.route('/jobs', methods=['GET'])
def list_jobs():
    try:
        print("📄 Fetching job roles from Excel...")
        return jsonify(get_all_jobs())
    except Exception as e:
        print(f"❌ Error in get_all_jobs(): {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/scan', methods=['POST'])
def scan_cvs():
    try:
        job_role = request.json.get('job')
        jd_summary = summarize_jd(job_role)
        shortlisted = []

        print(f"\n🔍 Scanning for job: {job_role}")
        print(f"📄 JD Summary:\n{jd_summary}")

        for file in os.listdir(CV_FOLDER):
            if file.endswith('.pdf'):
                path = os.path.join(CV_FOLDER, file)
                print(f"📄 Reading: {path}")

                cv_data = extract_cv_data(path)
                candidate_id = file.replace(".pdf", "")

                email = cv_data.get('email', "noemail@example.com")

                print(f"👤 {candidate_id} | {email}", end=" => ")

                score = match_score(jd_summary, cv_data)
                print(f"{score}%")

                if 100 >= score >= MATCH_THRESHOLD:
                    # ✅ Email + DB save
                    send_mail(cv_data['email'], job_role, candidate_id, score)


                    # ✅ Shortlist for UI
                    shortlisted.append({
                        'name': candidate_id,
                        'email': email,
                        'score': score
                    })

        print(f"✅ Total shortlisted: {len(shortlisted)}")
        return jsonify({'shortlisted': shortlisted})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
from database import init_db

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
