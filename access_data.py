from mistralai import Mistral
import os

# Most of this was generated from co piolot. I am still trying to 
# understand how to use Mistral API


# API KEY and PDF FILE
file = 'Invoice_2251071_from_FIBERLINK_CORP.pdf'
absolute_path = os.path.abspath(file)
api_key = os.environ.get("MISTRAL_API_KEY", "--")

# If the API key is not set
if not api_key:
    raise ValueError("API key not found. Please set the 'MISTRAL_API_KEY' environment variable.")

# Initialize the Minstral client with the API key
client = Mistral(api_key=api_key)

# Read the contents of the PDF file
with open(file, "rb") as pdf_file:
    pdf_content = pdf_file.read()

# Upload the PDF file to Mistral for processing
uploaded_pdf = client.files.upload(
    file={
        "file_name": file,
        "content": pdf_content,
    },
    purpose="ocr"
)

# Convert the uploaded_pdf object to a dictionary
uploaded_pdf_dict = uploaded_pdf.dict()
print("Uploaded PDF Response as Dictionary:")
print(uploaded_pdf_dict)

# Access specific attributes
file_id = uploaded_pdf_dict.get("id")  # Assuming "id" is the file ID
print(f"File ID: {file_id}")

# Retrieve the interpreted data using the file ID
if file_id:
    response = client.files.retrieve(file_id=file_id)
    print("Retrieved Response:")
    print(response)

    # Convert the response to a dictionary if needed
    if hasattr(response, "dict"):
        response_dict = response.dict()
        print("Retrieved Response as Dictionary:")
        print(response_dict)

        # Access the extracted data
        extracted_data = response_dict.get("data", {})
        print("Extracted Data:")
        print(extracted_data)
    else:
        print("The response object does not have a 'dict' method.")
else:
    print("File ID not found in the uploaded PDF response.")




if __name__ == '__main__':
    print('Running pdf extraction...')

    
    print('DONE!')