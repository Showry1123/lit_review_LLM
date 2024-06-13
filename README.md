## Project name: Research Abstract Summary App
Author: Showry Peng 

Contact: xpeng32@jh.edu |  [linkedin_SPeng](https://www.linkedin.com/in/showrypeng/)

Objective: This project aims to improve the efficiency of conducting literature review by simplify paper screening.

Instructions: This application has 3 different versions which are able to run on MacOS, WindowsOS and broswers. You can simply download the executive packages to run it. Or you can choose to run it in your browser, but this way will be more complicated.

*Most importantly, this app will run on your computer locally and never store your data and API except what you send to openai, which are the .txt file and your requests.

## Executive App 
Download from here [MacOS](https://drive.google.com/file/d/1noQj8qnohIlzFrcv-JIhXOIANV1fnmuM/view?usp=sharing) or [Win](https://drive.google.com/file/d/1K4VU_cn1M-lI3WTUG4g0IAzFA483ZihB/view?usp=sharing)

1. Firstly you need to download all the papers that you want to explore from PubMed as a .txt file (currently only PubMed supported). 
2. Run your app and insert your openai API.
3. Then upload your text file.
4. In the first box, fill with what you want chatGPT to summarize from every paper.
5. Set your maximum number of words output (you don't want to waste your money).
6. The third box input is optional, depending on whether you want to limit the summary output. It's like giving a dictionary to chatGPT and tell it generate output based on this list.
7. Click on "generate", then you'll have a .csv downloading.
8. In the csv file, you would see titles, authors, DOI, abstract and the summary of what you requested.

## Web App: 
1. Firstly you need to download all the papers that you want to explore from PubMed as a .txt file (currently only PubMed supported). 
2. Set openai API key as my_sk in .env (create a new file) and run app.py
3. Now you are on the app interface, then upload your text file.
4. In the first box, fill with what you want chatGPT to summarize from every paper.
5. Set your maximum number of words output (you don't want to waste your money).
6. The third box input is optional, depending on whether you want to limit the summary output. It's like giving a dictionary to chatGPT and tell it generate output based on this list.
7. Click on "generate", then you'll have a .csv downloading.
8. In the csv file, you would see titles, authors, DOI, abstract and the summary of what you requested.

Watch instruction video on using web app [here](https://drive.google.com/file/d/1xgkhhTIjsc4-3qv3LRe2aZGZOF2Sh7yH/view?usp=sharing)


Condition example for study type: Case-Control Studies, Systematic Review, Observation, Case Studies, Longitudinal Design, Cohort Study, Case Report, Experiments, Correlation, Preclinical Studies, Experimental Design, Randomized Controlled Trial, Cross-Sectional Studies,, Meta-Analysis, Descriptive Design, Animal Studies, Prospective Study
