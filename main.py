from fastapi import FastAPI, HTTPException
import requests
import pdfplumber

app = FastAPI()

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    return text

def extract_text_from_txt(txt_path: str) -> str:
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing TXT: {str(e)}")

@app.get("/extract_text/")
def extract_text(file_url: str):
    try:
        response = requests.get(file_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Unable to download file")
        
        content_type = response.headers.get("Content-Type", "").lower()
        temp_file = "temp_downloaded_file"
        
        with open(temp_file, "wb") as f:
            f.write(response.content)
        
        if "pdf" in content_type or file_url.endswith(".pdf"):
            text = extract_text_from_pdf(temp_file)
        elif "text" in content_type or file_url.endswith(".txt"):
            text = extract_text_from_txt(temp_file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        return {"text": text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
