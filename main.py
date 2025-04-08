'''
TODO: 
- Take in files from G drive
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
from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse
from pathlib import Path
import shutil
import base64
from http import client
import json
from pathlib import Path
from mistralai import Mistral, ImageURLChunk, TextChunk
from enum import Enum
from pathlib import Path
from pydantic import BaseModel
import base64
from PIL import Image


# Cant get working
def get_g_drive():
    pass


# Finds the path for a directory
def find_directory_path(target, start=r"C:\\"):
    ## Parameters
    #target = r"DOCUMENTS"
    #start = "C:\\"
    ## Parameters
    result = None
    for root, dirs, files in os.walk(start):
        if target in dirs:
            result = os.path.join(root, target)
    if result:
        print(f"Directory found: {result}\n")
        return result
    else:
        print(f"Directory not found.\n")
        return []


# Returns a list of files from a directory
def get_files_in_directory(directory):
    ## Parameters
    # directory = r"C:\Users\aiden\File Reader\DOCUMENTS"
    ## Parameters
    try:
        items = os.listdir(directory)
        files = [os.path.join(directory, item) for item in items if os.path.isfile(os.path.join(directory, item))]
        return files
    except FileNotFoundError:
        print("The specified directory does not exist.")
        return []


# Returns a dictionary holding the files path and the files content
def get_file_contents(files):
    files_read = {}
    for file in files:
        name, extension = os.path.splitext(os.path.basename(file))
        if extension == '.pdf':
            #print(f'PDF File: {name}')
            # content = read_pdf(file)
            files_read[file] = "This is the content inside a PDF file"
        else:
            #print(f'Skip File: {name}')
            files_read[file] = "This is the content inside other files"
    return files_read

    
# Returns the contents of a PDF file as a string
def read_pdf(file):
    api_key = "HLZgmBN1xuTeaA3XRNjQza9SjUP6M267"
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
            markdown_str = markdown_str.replace(
                f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
            )
        return markdown_str

    combined_markdown = get_combined_markdown(pdf_response)
    return combined_markdown


# Returns a string with png contents
def read_png(file):
    api_key = "HLZgmBN1xuTeaA3XRNjQza9SjUP6M267"
    client = Mistral(api_key=api_key)

    class StructuredOCR(BaseModel):
        file_name: str  # can be any string
        topics: list[str]  # must be a list of strings
        languages: str  # string
        ocr_contents: dict  # any dictionary, can be freely defined by the model

    def structured_ocr(image_path: str) -> StructuredOCR:
        image_file = Path(image_path)
        assert image_file.is_file(), "The provided image path does not exist."

        # Read and encode the image file
        encoded_image = base64.b64encode(image_file.read_bytes()).decode()
        base64_data_url = f"data:image/jpeg;base64,{encoded_image}"

        # Process the image using OCR
        image_response = client.ocr.process(
            document=ImageURLChunk(image_url=base64_data_url),
            model="mistral-ocr-latest"
        )
        image_ocr_markdown = image_response.pages[0].markdown

        # Parse the OCR result into a structured JSON response
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

    image_path = os.path.basename(file) # Path to sample receipt image
    structured_response = structured_ocr(Path(image_path)) # Process image and extract data

    # Parse and return JSON response
    response_dict = json.loads(structured_response.model_dump_json())
    string = image_string(response_dict)
    return string


# Creates a markdown file
def create_a_markdown_file(): ## MIGHT DELETE
    ## Parameters
    string = '# INVOICE \n\nFIBERLINK CORP\n304 Indian Trace \\#110\nWeston, FL 33326\n\n## Bill to\n\n2Midtown1210\nTyler Schultz\n3470 E Coast Ave\nApt. 1012\nMiami, FL 33137\n\n## Ship to\n\n2Midtown1210\nTyler Schultz\n3470 E Coast Ave\nApt. 1012\nMiami, FL 33137\n\n## Invoice details\n\nInvoice no.: 2251071\nTerms: Due on receipt\nInvoice date: 03/20/2025\nDue date: 03/20/2025\n\n|  | Date | Product or service | Description | Qty | Rate | Amount |\n| :--: | :--: | :--: | :--: | :--: | :--: | :--: |\n|  |  | INTERNET/Monthly | Monthly Internet Service | 1 | \\$60.00 | \\$60.00 |\n| Ways to pay |  |  |  |  |  |  |\n|  |  |  |  |  |  |  |\n\nNote to customer\nMail check to:\nFIBERLINK CORP\n304 Indian Trace \\#110\nWeston, FL 33326\n\nView and pay'
    file_path = r'C:\\Users\\aiden\\File Reader\\DOCUMENTS\\Invoice_2251071_from_FIBERLINK_CORP.pdf'
    # Parameters
    file = os.path.basename(file_path)
    name, extension = os.path.splitext(file)
    output_file = f'{name}.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(string)
    print(f"Markdown content has been saved to: {output_file}")
    return output_file


# Returns the path and content of each markdown file created
def create_markdown_files(files_read):
    markdown_files = {}
    for path, string in files_read.items():
        name, extension = os.path.splitext(os.path.basename(path))
        output_file = f'{name}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(string)
        output_path = move_markdown_file(output_file)
        markdown_files[output_path] = string
    return markdown_files   


# Moves the markdown files to a new directory and returns the files path
def move_markdown_file(source):
    new_dir = os.path.abspath(source)
    try:
        os.makedirs("Markdown Files", exist_ok=True)
    except:
        print('ERROR')
    new_dir = os.path.abspath("Markdown Files")
    shutil.move(source, new_dir)
    new_path = os.path.abspath(source)
    return new_path


# Returns a list of files that have the keyword in the file contents
def keyword_search(file_contents, keyword):
    ## Parameters
    #file_contents = ""
    #keyword = ""
    ## Parameters
    matches_found = {}
    for path, string in file_contents.items():
        if keyword in string:
            matches_found[path] = string
    return matches_found    

    
# Prints the items in a array neatly
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


# Converts dict from read_png() to a single string
def image_string(image):
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


# C:\Users\aiden\File Reader\DOCUMENTS
# C:\Users\aiden\SMURF ACCOUNT\SCRIPTS\TEST DUMMY

# C:\\Users\\aiden\\File Reader\\DOCUMENTS\\Invoice_2251071_from_FIBERLINK_CORP.pdf
#  # INVOICE \n\nFIBERLINK CORP\n304 Indian Trace \\#110\nWeston, FL 33326\n\n## Bill to\n\n2Midtown1210\nTyler Schultz\n3470 E Coast Ave\nApt. 1012\nMiami, FL 33137\n\n## Ship to\n\n2Midtown1210\nTyler Schultz\n3470 E Coast Ave\nApt. 1012\nMiami, FL 33137\n\n## Invoice details\n\nInvoice no.: 2251071\nTerms: Due on receipt\nInvoice date: 03/20/2025\nDue date: 03/20/2025\n\n|  | Date | Product or service | Description | Qty | Rate | Amount |\n| :--: | :--: | :--: | :--: | :--: | :--: | :--: |\n|  |  | INTERNET/Monthly | Monthly Internet Service | 1 | \\$60.00 | \\$60.00 |\n| Ways to pay |  |  |  |  |  |  |\n|  |  |  |  |  |  |  |\n\nNote to customer\nMail check to:\nFIBERLINK CORP\n304 Indian Trace \\#110\nWeston, FL 33326\n\nView and pay


if __name__ == "__main__":
    print('\nStart main.py...\n')

    '''
    # find_directory_path()
    files = get_files_in_directory()
    
    # read_files()
    for f in files:
        print(f)
    print()

    contents = get_file_contents(files)

    for i in contents:
        print(i)
        print()
    
    create_markdown()
    files = get_files_in_directory()
    #format_print(files)
    files_read = get_file_contents(files)
    matches = keyword_search(files_read, 'S')
    print()
    markdown_files = create_markdown_files(files_read)
    format_print(markdown_files)
    '''

    '''
    image = {
        "file_name": "parking_receipt",
        "topics": [
            "Parking",
            "Receipt",
            "City of Palo Alto"
        ],
        "languages": "English",
        "ocr_contents": {
            "header": "PLACE FACE UP ON DASH CITY OF PALO ALTO NOT VALID FOR ONSTREET PARKING",
            "expiration_date_time": "11:59 PM AUG 19, 2024",
            "purchase_date_time": "01:34pm Aug 19, 2024",
            "total_due": "$15.00",
            "rate": "Daily Parking",
            "total_paid": "$15.00",
            "payment_type": "CC (Swipe)",
            "ticket_number": "00005883",
            "serial_number": "520117260957",
            "setting": "Permit Machines",
            "machine_name": "Civic Center",
            "additional_info": "#^^^^-1224, Visa DISPLAY FACE UP ON DASH PERMIT EXPIRES AT MIDNIGHT"
        }
    }
    
    test = image_string(image)
    print(test)
    

    #print(file_contents)    
    '''

    print('\n...DONE\n')
