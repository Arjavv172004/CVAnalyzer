from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_score(jd_summary, cv_data):
    jd = jd_summary.lower().strip()
    cv = f"{cv_data['text']} {cv_data['email']}".lower().strip()

    if not jd or not cv:
        return 0.0

    emphasized_jd = (jd + " ") * 3

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform([emphasized_jd, cv])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    return round(score * 1000, 2)
