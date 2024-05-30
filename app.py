from flask import Flask, request, render_template, send_file, jsonify
from openai import OpenAI
import os
import re
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Split the content based on double newlines followed by a number and a period
def split_papers(text):
    papers = re.split(r'\n\n\d+\. ', text)
    papers[0] = papers[0][3:]
    return papers

# Extract paper information
def extract_paper_info(text):
    papers = split_papers(text)
    extracted_info = []

    for paper in papers:
        double_newlines = [match.start() for match in re.finditer(r'\n\n', paper)]
        title = "Title not found"
        if len(double_newlines) > 1:
            title = paper[double_newlines[0]:double_newlines[1]].strip()
        authors = "Authors not found"
        if len(double_newlines) > 2:
            authors = paper[double_newlines[1]:double_newlines[2]].strip()
        doi_match = re.search(r'\nDOI:\s*(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', paper, re.IGNORECASE)
        doi = doi_match.group(1).strip() if doi_match else "DOI not found"
        abstract = "Abstract not found"
        if '\n\nCopyright' in paper:
            copyright_position = paper.find('\n\nCopyright')
            last_double_newline_before_copyright = paper.rfind('\n\n', 0, copyright_position)
            if last_double_newline_before_copyright != -1:
                abstract = paper[last_double_newline_before_copyright:copyright_position].strip()
        elif '\n\n©' in paper:
            copyright_position = paper.find('\n\n©')
            last_double_newline_before_copyright = paper.rfind('\n\n', 0, copyright_position)
            if last_double_newline_before_copyright != -1:
                abstract = paper[last_double_newline_before_copyright:copyright_position].strip()
        elif '\n\nDOI:' in paper:
            doi_position = paper.find('\n\nDOI: ')
            last_double_newline_before_doi = paper.rfind('\n\n', 0, doi_position)
            if last_double_newline_before_doi != -1:
                abstract = paper[last_double_newline_before_doi:doi_position].strip()
        abstract = re.sub(r'\n', ' ', abstract)
        if 'Author information: ' in abstract or 'Comment ' in abstract or len(abstract.split()) < 5:
            abstract = 'Abstract not found'
        extracted_info.append({
            "Title": title,
            "Authors": authors,
            "DOI": doi,
            "Abstract": abstract
        })

    return extracted_info

# Function to get GPT response
def get_gpt_response(abstract, abstract_query, word_count, conditions):
    client = OpenAI(api_key=os.getenv('my_sk'))
    condition_text = f" You should only use the following answers: {conditions}. If none of the options are suitable, provide the best possible answer." if conditions else ""
    prompt = (f"You are an expert research assistant with extensive experience in biomedicine and health science, helping with a literature review for a research idea. You are adept at analyzing and summarizing scientific documents, including abstracts from various study designs such as randomized controlled trials, cohort studies, case-control studies, cross-sectional studies, and systematic reviews. Your task is to read and analyze the abstract provided and summarize the specific aspect requested by the user, considering the methodology, objectives, sample size, data collection techniques, and analysis methods used in the study."
              f"\n\nYou will be provided with an abstract of a scientific document. Summarize '{abstract_query}' with only {word_count} words:"
              f"{condition_text} \n\nAbstract:\n{abstract}")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.choices[0].message.content.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        abstract_query = request.form['abstract_query']
        word_count = request.form['word_count']
        conditions = request.form.get('conditions', '')

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            extracted_info = extract_paper_info(text)
            df = pd.DataFrame(extracted_info)

            df['Conclusion'] = df['Abstract'].apply(lambda abstract: get_gpt_response(abstract, abstract_query, word_count, conditions))
            csv_filename = f"{filename.split('.')[0]}_conclusions.csv"
            csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)

            df.to_csv(csv_filepath, index=False)

            return send_file(csv_filepath, as_attachment=True, mimetype='text/csv')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
