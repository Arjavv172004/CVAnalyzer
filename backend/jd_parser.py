import pandas as pd

def get_all_jobs():
    df = pd.read_excel('../job_description.xlsx')
    return df['Job Title'].dropna().unique().tolist()

def summarize_jd(job_role):
    df = pd.read_excel('../job_description.xlsx')
    jd_row = df[df['Job Title'] == job_role].iloc[0]
    return f"{jd_row['Job Description']}"
