from flask import Flask, render_template, request, redirect, url_for
import os
from resume_analyzer import clean_text  # your cleaning function to normalize text
from PyPDF2 import PdfReader
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================== Role Keywords ==================
ROLE_KEYWORDS = {
    'Data Scientist': ['python', 'machine learning', 'statistics', 'data analysis', 'pandas',
                       'numpy', 'visualization', 'sql', 'regression', 'classification',
                       'clustering', 'tensorflow', 'deep learning', 'nlp',
                       'big data', 'r', 'matplotlib', 'scikit-learn', 'data mining', 'hadoop'],
    
    'Software Engineer': ['java', 'c++', 'python', 'software development', 'algorithms',
                          'data structures', 'oop', 'git', 'rest api', 'sql',
                          'debugging', 'system design', 'agile', 'scrum', 'javascript',
                          'spring', 'html', 'css', 'linux', 'unit testing'],
    
    'Machine Learning Engineer': ['python', 'tensorflow', 'pytorch', 'model deployment',
                                  'machine learning', 'deep learning', 'scikit-learn',
                                  'data preprocessing', 'feature engineering', 'airflow',
                                  'mlops', 'docker', 'kubernetes', 'flask', 'api'],
    
    'AI Engineer': ['python', 'deep learning', 'nlp', 'tensorflow', 'pytorch', 'neural networks',
                    'transformers', 'chatbots', 'opencv', 'image processing',
                    'speech recognition', 'ml', 'scikit-learn', 'bert', 'openai'],
    
    'DevOps Engineer': ['aws', 'docker', 'kubernetes', 'ci/cd', 'terraform', 'ansible',
                        'linux', 'bash scripting', 'monitoring', 'jenkins', 'gitlab',
                        'cloudwatch', 'python', 'helm', 'infrastructure as code'],
    
    'Cloud Engineer': ['aws', 'azure', 'gcp', 'cloud computing', 'terraform', 'iac',
                       'devops', 'kubernetes', 'cloudformation', 'lambda', 'ec2',
                       's3', 'iam', 'cloudwatch', 'networking'],
    
    'Cybersecurity Analyst': ['network security', 'encryption', 'firewall', 'vulnerability',
                              'linux', 'risk assessment', 'incident response', 'python',
                              'wireshark', 'penetration testing', 'cybersecurity frameworks',
                              'siem', 'intrusion detection'],
    
    'Data Engineer': ['spark', 'hadoop', 'etl', 'airflow', 'data pipelines', 'big data',
                      'sql', 'nosql', 'python', 'scala', 'aws', 's3', 'glue', 'kafka',
                      'data warehouse', 'snowflake', 'databricks'],
    
    'Backend Developer': ['node.js', 'python', 'java', 'sql', 'rest api', 'mongodb',
                          'express', 'server-side', 'authentication', 'jwt',
                          'unit testing', 'docker', 'graphql', 'redis'],
    
    'Frontend Developer': ['html', 'css', 'javascript', 'react', 'vue', 'angular',
                           'responsive design', 'redux', 'bootstrap', 'typescript',
                           'ui/ux', 'sass', 'web components'],
    
    'Full Stack Developer': ['html', 'css', 'javascript', 'react', 'node.js', 'python',
                             'sql', 'rest api', 'mongodb', 'flask', 'django',
                             'express', 'git', 'docker', 'unit testing'],
    
    'System Administrator': ['linux', 'windows', 'bash scripting', 'networking',
                             'vmware', 'troubleshooting', 'dns', 'active directory',
                             'firewall', 'monitoring', 'backup', 'security'],
    
    'Business Analyst': ['data analysis', 'requirements gathering', 'sql', 'excel',
                         'uml', 'user stories', 'stakeholder communication',
                         'dashboard', 'powerbi', 'tableau', 'process modeling'],
    
    'Database Administrator': ['sql', 'oracle', 'performance tuning', 'backup',
                                'recovery', 'data modeling', 'indexes', 'postgresql',
                                'mysql', 'replication', 'security'],
    
    'QA Engineer': ['test cases', 'selenium', 'manual testing', 'automation testing',
                    'python', 'java', 'bug tracking', 'jira', 'api testing', 'unit testing'],
    
    'Mobile Developer': ['android', 'kotlin', 'ios', 'swift', 'flutter', 'react native',
                         'mobile ui', 'rest api', 'firebase', 'play store', 'app store'],
    
    'UX Designer': ['figma', 'wireframing', 'prototyping', 'user research', 'ux design',
                    'ui design', 'accessibility', 'adobe xd', 'sketch', 'interaction design'],
    
    'IT Support Specialist': ['helpdesk', 'vpn', 'windows', 'hardware', 'networking',
                              'troubleshooting', 'tickets', 'active directory',
                              'remote support', 'printers', 'microsoft office'],
    
    'Network Engineer': ['routing', 'switching', 'firewalls', 'network design',
                         'tcp/ip', 'dns', 'vpn', 'lan/wan', 'network monitoring',
                         'cisco', 'load balancing'],
    
    'AI Researcher': ['deep learning', 'nlp', 'transformers', 'research papers',
                      'python', 'tensorflow', 'pytorch', 'gpt', 'attention mechanism',
                      'data preprocessing']
}

# ================== Certificate Links ==================
CERTIFICATE_LINKS = {
    'python': 'https://www.coursera.org/specializations/python',
    'machine learning': 'https://www.coursera.org/learn/machine-learning',
    'statistics': 'https://www.khanacademy.org/math/statistics-probability',
    'sql': 'https://www.datacamp.com/courses/sql-for-data-scientists',
    'tensorflow': 'https://www.coursera.org/learn/introduction-tensorflow',
    'deep learning': 'https://www.deeplearning.ai/deep-learning-specialization/',
    'pytorch': 'https://pytorch.org/tutorials/',
    'aws': 'https://www.aws.training/Details/Curriculum?id=20685',
    'docker': 'https://www.udemy.com/course/docker-mastery/',
    'kubernetes': 'https://www.coursera.org/learn/google-kubernetes-engine',
    'react': 'https://www.codecademy.com/learn/react-101',
    'node.js': 'https://nodejs.dev/en/learn',
    'html': 'https://developer.mozilla.org/en-US/docs/Web/HTML',
    'css': 'https://developer.mozilla.org/en-US/docs/Web/CSS',
    'git': 'https://www.coursera.org/learn/introduction-git-github',
    'airflow': 'https://www.astronomer.io/guides/what-is-apache-airflow/',
    'java': 'https://www.coursera.org/specializations/java-programming',
    'c++': 'https://www.learncpp.com/',
    'nlp': 'https://www.coursera.org/learn/language-processing',
    'linux': 'https://linuxjourney.com/',
    'flask': 'https://flask.palletsprojects.com/en/2.0.x/tutorial/',
    'azure': 'https://learn.microsoft.com/en-us/training/azure/',
    'gcp': 'https://cloud.google.com/training',
    'scrum': 'https://www.scrum.org/resources/what-is-scrum',
    'data structures': 'https://www.geeksforgeeks.org/data-structures/',
    'oop': 'https://www.udacity.com/course/software-engineering-process--ud805'
}


jobs_df = pd.read_csv('data/job_opportunities.csv')

def extract_text_from_pdf(filepath):
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() + " "
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def get_resume_keywords(text):
    # This should return a list of keywords extracted from resume text.
    # Here we just split by whitespace and lowercase, or you can do better NLP keyword extraction.
    words = set(clean_text(text).split())
    return list(words)

def analyze_resume(role, resume_keywords):
    role_keywords = ROLE_KEYWORDS.get(role, [])
    role_set = set(k.lower() for k in role_keywords)
    resume_set = set(k.lower() for k in resume_keywords)

    matched = resume_set.intersection(role_set)
    missing = role_set.difference(resume_set)

    ats_score = (len(matched) / len(role_set)) * 100 if role_set else 0

    # Certificate suggestions for missing skills
    cert_recommendations = {skill: CERTIFICATE_LINKS.get(skill, "No cert available") for skill in missing}

    # Recommend jobs that require the role or any matched skill
    filtered_jobs = jobs_df[
        (jobs_df['Job Title'].str.contains(role, case=False, na=False)) |
        (jobs_df['Required Skills'].apply(lambda x: any(skill in x.lower() for skill in matched)))
    ].head(5)

    return {
        'ats_score': ats_score,
        'matched_skills': sorted(matched),
        'missing_skills': sorted(missing),
        'cert_recommendations': cert_recommendations,
        'recommended_jobs': filtered_jobs.to_dict(orient='records')
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        role = request.form.get('role')
        file = request.files.get('resume')

        if not role or not file:
            return render_template('index.html', error="Please select a role and upload your resume.")

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        resume_keywords = get_resume_keywords(text)

        analysis = analyze_resume(role, resume_keywords)

        return render_template('result.html', role=role, analysis=analysis)

    roles = list(ROLE_KEYWORDS.keys())
    return render_template('index.html', roles=roles)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5554, debug=True)