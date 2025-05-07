'''
TODO: 
- Take in files # from G drive
- Take in files of various types
- Read the file contents
- Convert the contents into a markdown string and store it
- Create a markdown file with the file contents
- Search the file contents for keywords
- Way for user to use the functions


get_g_drive() - Not Working
find_directory_path() - Slow but works
read_png() - Needs more testing
create_a_markdown_file() - Not being used (redundant)
image_string() - Needs more testing
'''

import os
import io
import json
import shutil
import base64
from PIL import Image
from enum import Enum
from http import client
from pydantic import BaseModel
from pathlib import Path
from mistralai import Mistral, ImageURLChunk, TextChunk,  DocumentURLChunk
from mistralai.models import OCRResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Global Variables
Mistral_API = 'HLZgmBN1xuTeaA3XRNjQza9SjUP6M267'
G_Drive = 'https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link'
Credentials_Json = r'C:\Users\aiden\File Reader\Demo Project\file-reader-456206-7659069c7d5d.json'
Download_Dir = r'C:\Users\aiden\File Reader\Demo Project\G Drive Files'
Markdown_Dir = r"C:\Users\aiden\File Reader\Demo Project\Markdown Files"



# Gets the folder id from the folder link
def get_folder_id(link):
    result = link.split(r'folders/')[1].split('?')[0]
    return result


# Downloads the files from a G drive
def download_gdrive_files():
    folder_id = get_folder_id(G_Drive)
    download_dir = Download_Dir
    service_file = Credentials_Json
    scope = ['https://www.googleapis.com/auth/drive']
    os.makedirs(download_dir, exist_ok=True)

    credentials = service_account.Credentials.from_service_account_file(service_file, scopes=scope)
    drive_service = build('drive', 'v3', credentials=credentials)
    query = f"'{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    for file in files:
        file_path = os.path.join(download_dir, file['name'])
        request = drive_service.files().get_media(fileId=file['id'])
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            # print(f"Downloading: {file['name']}")

    return download_dir
    

# Returns a list of files from a directory
def load_directory_files(directory):
    try:
        items = os.listdir(directory)
        files = [os.path.join(directory, item) for item in items if os.path.isfile(os.path.join(directory, item))]
        return files
    except FileNotFoundError:
        print("The specified directory does not exist.")
        return []


# Creates a description of the given image
def describe_image(base64_str):
        return "Image Description Here"


# Returns PDF file contents as a string
def read_pdf(file):
    api_key = Mistral_API
    client = Mistral(api_key=api_key)
    pdf_file = Path(file)

    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
        )
    
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    
    pdf_response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True
    )

    def get_combined_markdown(ocr_response: OCRResponse) -> str:
        markdowns: list[str] = []
        for page in ocr_response.pages:
            image_data = {}
            for img in page.images:
                image_data[img.id] = img.image_base64
            markdowns.append(replace_images_in_markdown(page.markdown, image_data))
        return "\n\n".join(markdowns)
    
    def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:    
        for img_name, base64_str in images_dict.items():
            img_desc = describe_image(base64_str)
            markdown_str = markdown_str.replace(
                f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})\n[{img_desc}]\n"
            )
        return markdown_str

    combined_markdown = get_combined_markdown(pdf_response)
    return combined_markdown


# Returns PNG file contents as a string
def read_png(file):
    api_key = Mistral_API
    client = Mistral(api_key=api_key)

    class StructuredOCR(BaseModel):
        file_name: str
        topics: list[str]
        languages: str
        ocr_contents: dict
    
    def structured_ocr(image_path: str) -> StructuredOCR:
        image_file = Path(image_path)
        assert image_file.is_file(), "The provided image path does not exist."
        encoded_image = base64.b64encode(image_file.read_bytes()).decode()
        base64_data_url = f"data:image/jpeg;base64,{encoded_image}"
        
        image_response = client.ocr.process(
            document=ImageURLChunk(image_url=base64_data_url),
            model="mistral-ocr-latest"
        )

        image_ocr_markdown = image_response.pages[0].markdown
        
        chat_response = client.chat.parse(
            model="pixtral-12b-latest",
            messages=[
                {
                    "role": "user",
                    "content": [
                        ImageURLChunk(image_url=base64_data_url),
                        TextChunk(text=(
                            f"This is the image's OCR in markdown:\n{image_ocr_markdown}\n.\n"
                            "Convert this into a structured JSON response "
                            "with the OCR contents in a sensible dictionnary."
                            )
                        )
                    ]
                }
            ],
            response_format=StructuredOCR,
            temperature=0
        )

        return chat_response.choices[0].message.parsed

    def get_png_markdown(image):
        string = []
        for key, value in image.items():
            if type(value) == list:
                string.append(f'\n{key}:')
                for i in value:
                    string.append(f'- {i}')
            elif type(value) == dict:
                string.append(f'\n{key}:')
                for k, v in value.items():
                    string.append(f'- {k} : {v}')
            else:
                string.append(f'\n{key} : {value}')
        return "\n".join(string)

    image_path = os.path.basename(file)
    structured_response = structured_ocr(Path(file))
    response_dict = json.loads(structured_response.model_dump_json())
    string = get_png_markdown(response_dict)
    return string


# Returns a dictionary holding the files path and the files content
def extract_file_data(files):
    files_read = {}
    for file in files:
        name, extension = os.path.splitext(os.path.basename(file))
        if extension == '.pdf':
            content = 'This is the content of a PDF file.'
            # content = read_pdf(file)
            files_read[file] = content
            
        elif extension == '.png':
            content = 'This is the content of a PNG file.'
            # content = read_png(file)
            files_read[file] = content
    return files_read


# Returns the path and content of each Markdown file created
def generate_markdown_files(file_data):
    md_data = {}
    md_dir = Markdown_Dir
    os.makedirs(md_dir, exist_ok=True)

    for path, string in file_data.items():
        name, type = os.path.splitext(os.path.basename(path))
        md_name = f'{name}.md'
        md_path = os.path.join(md_dir, md_name)
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(string)
        md_data[md_path] = string

    return md_data


# Returns a list of files that match the keyword
def keyword_search(file_contents, keyword):
    matches_found = {}
    for path, string in file_contents.items():
        if keyword in string:
            matches_found[path] = string
    return matches_found    

    
# Prints the array neatly
def format_print(files):
    for file in files:
        if type(files) == list:
            print(file)
            format_print(file)
        elif type(files) == dict:
            print(file)
            print(files[file])
            format_print(files[file])
        else:
            print()
            break
    

# Order of wich to call functions
def main():
    print('\nHello!\n')
    # user = input('Pleaser enter your google drive link:\n')
    # global G_Drive
    # G_Drive = user

    print('\n...Downloading Files...')
    gdrive_dir = download_gdrive_files()

    print('\n...Processing Files...')
    file_list = load_directory_files(gdrive_dir)

    file_data = extract_file_data(file_list)

    print('\n...Generating Files...')
    markdown_files = generate_markdown_files(file_data)


if __name__ == "__main__":
    main()




# TODO
# Debug read_png()
# Take in variables
# Create global variables
# Open AI image reader
# Readme file
# Ask user what to do
# Improve keyword search
# Get variables if the user asks for

    # Mandatory Variables:
    # - Mistral API key
    # - Google drive folder id
    # - Google credential json
    # - Install directory
    # - Markdown Directory
