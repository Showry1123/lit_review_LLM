import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
from openai import OpenAI
import re
import webbrowser
import datetime
import sys


sys.setrecursionlimit(2000)  # Default is usually 1000


directory = "uploads"
if not os.path.exists(directory):
    os.makedirs(directory)

root = tk.Tk()
root.title("Abstract Summary App")
root.geometry("600x600")

status_label = tk.Label(root, text="")
status_label.pack(side="bottom", fill="x", anchor="w")

# Global variable to store the file path
global file_path
file_path = None

# API Key Entry
api_key_label = tk.Label(root, text="Enter API Key (the app runs locally and won't be stored):")
api_key_label.pack()
api_key_entry = tk.Entry(root, bd=5)
api_key_entry.pack()

def ask_for_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=f"Selected file: {os.path.basename(file_path)}")

upload_button = tk.Button(root, text="Upload File", command=ask_for_file)
upload_button.pack()
file_label = tk.Label(root, text="No file selected")
file_label.pack()

abstract_query_label = tk.Label(root, text="What do you want to conclude from the abstract?")
abstract_query_label.pack()
abstract_query_entry = tk.Entry(root, bd=5)
abstract_query_entry.pack()

word_count_label = tk.Label(root, text="How many words in the conclusion?")
word_count_label.pack()
word_count_entry = tk.Entry(root, bd=5)
word_count_entry.pack()

conditions_label = tk.Label(root, text="Conditions (optional):")
conditions_label.pack()
conditions_entry = tk.Entry(root, bd=5)
conditions_entry.pack()


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


def process_and_generate(file_path, api_key, abstract_query, word_count, conditions):
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Extract paper information using your previously defined function
        extracted_info = extract_paper_info(text)
        df = pd.DataFrame(extracted_info)

        # Initialize the API client
        client = OpenAI(api_key=api_key)

        # Process each abstract and generate conclusions
        df['Conclusion'] = df['Abstract'].apply(
            lambda abstract: get_gpt_response(client, abstract, abstract_query, word_count, conditions)
        )

        # Generate a timestamp string
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        # Use the timestamp in the filename to ensure uniqueness
        csv_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_conclusions_{timestamp}.csv"
        csv_filepath = os.path.join('uploads', csv_filename)
        df.to_csv(csv_filepath, index=False)

        # Notify user of success
        messagebox.showinfo("Success", f"CSV generated successfully at {csv_filepath}")

    except Exception as e:
        # Handle errors
        messagebox.showerror("Error", str(e))

def get_gpt_response(client, abstract, abstract_query, word_count, conditions):
    # Construct the prompt
    condition_text = f" You should only use the following answers: {conditions}. If none of the options are suitable, provide the best possible answer." if conditions else ""
    prompt = (f"You are an expert research assistant with extensive experience in biomedicine and health science, helping with a literature review for a research idea. You are adept at analyzing and summarizing scientific documents. Your task is to read and analyze the abstract provided and summarize the specific aspect requested by the user, considering the methodology, objectives, sample size, data collection techniques, and analysis methods used in the study."
              f"\n\nYou will be provided with an abstract of a scientific document. Summarize '{abstract_query}' with only {word_count} words:"
              f"{condition_text} \n\nAbstract:\n{abstract}")

    # Generate response from GPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.choices[0].message.content.strip()



def generate_csv():
    global file_path
    if file_path and os.path.exists(file_path):
        try:
            process_and_generate(file_path, api_key_entry.get(), abstract_query_entry.get(), 
                                 word_count_entry.get(), conditions_entry.get())
            messagebox.showinfo("Success", "CSV file generated successfully.")
            status_label.config(text="Download complete!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Failed to generate CSV.", fg="red")
    else:
        messagebox.showerror("Error", "No file selected or file does not exist.")

generate_button = tk.Button(root, text="Generate CSV", command=generate_csv)
generate_button.pack(pady=20)





def send_email():
    try:
        webbrowser.open("mailto:xpeng32@jh.edu?Subject=Hello%20from%20Your%20App")
    except Exception as e:
        messagebox.showerror("Error", "Failed to open email client: " + str(e))

def open_linkedin():
    try:
        webbrowser.open("https://www.linkedin.com/in/showrypeng/")
    except Exception as e:
        messagebox.showerror("Error", "Failed to open LinkedIn: " + str(e))

def open_donation_link():
    webbrowser.open('https://www.paypal.com/paypalme/yoshowry')


# Frame for contact information
contact_frame = tk.Frame(root)
contact_frame.pack(side="top", fill="x", expand=True)

# Developer information
personal_info_label = tk.Label(contact_frame, text="Developed by: Showry Peng", fg="grey")
personal_info_label.pack(side="top", pady=(20, 0))

# Contact and feedback information
contact_label = tk.Label(contact_frame, text="If you have any questions or feedbacks, please contact:", fg="grey")
contact_label.pack(side="top", pady=(10, 0))

# Links frame
links_frame = tk.Frame(contact_frame)
links_frame.pack(side="top", pady=(10, 0))

# Email and LinkedIn links
email_button = tk.Button(links_frame, text="Email: xpeng32@jh.edu", command=send_email, fg="blue", cursor="hand2", relief="flat")
email_button.pack(side="left", padx=10)
linkedin_button = tk.Button(links_frame, text="LinkedIn: Showry Peng", command=open_linkedin, fg="blue", cursor="hand2", relief="flat")
linkedin_button.pack(side="left", padx=10)

# Donation support
support_label = tk.Label(contact_frame, text="Thanks for your support!", fg="grey")
support_label.pack(side="top", pady=(10, 0))

donate_button = tk.Button(contact_frame, text="Donate via PayPal", command=open_donation_link, fg="blue", cursor="hand2", relief="flat")
donate_button.pack(side="top", pady=(0, 20))

root.mainloop()
