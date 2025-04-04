"""
Description: This file asks the user to enter an API Key and a PDF File. Using the given inputs, the Mistral client is initialized and the existence of the PDF File 
is checked. The OCR then extracts the text (in Markdown format) and the images (Base64-encoded) from the uploaded PDF. The extracted data is then 
processed and formated into a single Markdwon string. Which is then uploaded to a Markdown file with the same name as the uploaded PDF.

TODO:
  - Error messages if api key or pdf file is invalid
  - Main function
  - Polish up code
  - Add/Change some comments for better explination
  - Structure directory
"""

# Libraries
from pathlib import Path
from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse


# API key
api_key = "_____"

# File path
pdf_file = Path("____")

# Mistral client
client = Mistral(api_key=api_key)


# Verifies the file exists
try:
    assert pdf_file.is_file()
except AssertionError:
    print(f"File [{pdf_file}] does not exist.")

# Stores the response after Uploading the PDF file to Mistrals servers
uploaded_file = client.files.upload(
    file={
        "file_name": pdf_file.stem,
        "content": pdf_file.read_bytes(),
    },
    purpose="ocr",
)

# Stores a temporary, secure URL that allows access to the uploaded PDF file on Mistrlals servers
signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

# Stores the results of the OCR process from the uploaded PDF file
pdf_response = client.ocr.process(
    document=DocumentURLChunk(document_url=signed_url.url),
    model="mistral-ocr-latest",
    include_image_base64=True
)



# Combines the extracted text and images from the OCR response into a single string in Markdown format
def get_combined_markdown(ocr_response: OCRResponse) -> str:
    markdowns: list[str] = []

    # Creates a new empty dictionary for each page in the OCR response
    for page in ocr_response.pages:
        image_data = {}

        # Iterates through each image on the page and stores the base64 image data
        for img in page.images:
            image_data[img.id] = img.image_base64

        # Appends the result of the function to the markdowns list
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))

    # Combines all the Markdown strings into a single string
    return "\n\n".join(markdowns)



# Replaces the image placeholders in the Markdown string with their corresponding base64-encoded image data
def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
        )

    # Returns the modified Markdown string
    return markdown_str



# Get the combined Markdown content from the OCR response
combined_markdown = get_combined_markdown(pdf_response)

# Create the name of the Markdown file
output_file = f'{pdf_file.stem}.md'

# Write the combined Markdown content to a file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(combined_markdown)

# Print the location of the saved Markdown file
print(f"Markdown content has been saved to: {output_file}")
