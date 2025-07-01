import json
import requests

def fetch_job_data(job_fit_dict):
    max_fit = 0
    selected_job = ""
    for job, fit in job_fit_dict.items():
        if fit > max_fit:
            max_fit = fit
            selected_job = job

    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": f"{selected_job}","page":"1","num_pages":"1","country":"in","date_posted":"all"}

    headers = {
        "x-rapidapi-key": "0fe32ee739msh3a330024e2144e4p199f0fjsn15ac34ed5354",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    with open("./uploads/resume.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    data['job_openings'] = response.json().get('data', [])

    with open("./uploads/resume.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

with open("./uploads/resume.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
    job_fit_dict = data.get('job_roles', {})

fetch_job_data(job_fit_dict)

