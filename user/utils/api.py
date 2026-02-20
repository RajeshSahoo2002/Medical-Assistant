import requests
from config import API_URL

def upload_pdfs_api(files):
    # Below function is mainly for the getting the payload or the body is to upload the pdf files to the backend server using the API endpoint and f.name is to capture the file name, f.read is to make the file read and application/pdf is for ensuring only .pdf files are uploaded to as dataset to the backend
    files_payload=[("files",(f.name,f.read(),"application/pdf"))for f in files]
    return requests.post(f"{API_URL}/upload_pdfs/",files=files_payload)
    
def ask_question(question):
    return requests.post(f"{API_URL}/ask/",data={"question":question}) # type: ignore