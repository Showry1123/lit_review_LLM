## Project name: Research Abstract Summary App
## Author: Showry Peng

## Objective: This project aims to improve the efficiency of conducting literature review by simplify paper screening.
## Instruction: 
1. Firstly you need to download all the papers that you want to explore from PubMed as a .txt file (currently only PubMed supported). 
2. Set openai API key as my_sk in .env and run app.py
3. Now you are on the app interface, then upload your text file.
4. In the first box, fill with what you want chatGPT to summarize from every paper.
5. Set your maximum number of words output (you don't want to waste your money).
6. The third box input is optional, depending on whether you want to limit the summary output. It's like giving a dictionary to chatGPT and tell it generate output based on this list.
7. Click on "generate", then you'll have a .csv downloading.
8. In the csv file, you would see titles, authors, DOI, abstract and the summary of what you requested.


Watch instruction video [here](https://drive.google.com/file/d/1xgkhhTIjsc4-3qv3LRe2aZGZOF2Sh7yH/view?usp=sharing)


condition example: Case-Control Studies, Systematic Review, Observation, Case Studies, Longitudinal Design, Cohort Study, Case Report, Experiments, Correlation, Preclinical Studies, Experimental Design, Randomized Controlled Trial, Cross-Sectional Studies,, Meta-Analysis, Descriptive Design, Animal Studies, Prospective Study
