### OCR with uploaded PDF file using Mistral API from Mistral Doc ###
from mistralai import Mistral
import os

# Mistral API key
api_key = os.environ["MISTRAL_API_KEY"]

# Initialize the Mistral client with the API key
client = Mistral(api_key=api_key)

# Upload a PDF file for OCR processing
uploaded_pdf = client.files.upload(
    file={
        "file_name": "uploaded_file.pdf",
        "content": open("uploaded_file.pdf", "rb"),
    },
    purpose="ocr"
)  

# Retrieve file
client.files.retrieve(file_id=uploaded_pdf.id)

'''
id='00edaf84-95b0-45db-8f83-f71138491f23' 
object='file' 
size_bytes=3749788 
created_at=1741023462 
filename='uploaded_file.pdf' 
purpose='ocr' 
sample_type='ocr_input' 
source='upload' 
deleted=False 
num_lines=None'
'''

# Get the signed URL
signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)


# Get OCR results
import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": signed_url.url,
    }
)