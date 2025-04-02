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

# Import required libraries
from mistralai import Mistral
from pathlib import Path
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk
import json
from mistralai.models import OCRResponse


# Initialize Mistral client with API key
api_key = input("Enter your Mistral API key: ")
client = Mistral(api_key=api_key)

# Verify PDF file exists
pdf_file = Path(input("Enter the name of the PDF file: "))
assert pdf_file.is_file()


# Upload PDF file to Mistral's OCR service
uploaded_file = client.files.upload(
    file={
        "file_name": pdf_file.stem,
        "content": pdf_file.read_bytes(),
    },
    purpose="ocr",
)

# Get URL for the uploaded file
signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

# Process PDF with OCR, including embedded images
pdf_response = client.ocr.process(
    document=DocumentURLChunk(document_url=signed_url.url),
    model="mistral-ocr-latest",
    include_image_base64=True
)

# Convert response to JSON format
response_dict = json.loads(pdf_response.model_dump_json())

# print(json.dumps(response_dict, indent=4)[0:1000]) # check the first 1000 characters


def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    """
    Replace image placeholders in markdown with base64-encoded images.

    Args:
        markdown_str: Markdown text containing image placeholders
        images_dict: Dictionary mapping image IDs to base64 strings

    Returns:
        Markdown text with images replaced by base64 data
    """
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
        )
    return markdown_str

def get_combined_markdown(ocr_response: OCRResponse) -> str:
    """
    Combine OCR text and images into a single markdown document.

    Args:
        ocr_response: Response from OCR processing containing text and images

    Returns:
        Combined markdown string with embedded images
    """
    markdowns: list[str] = []
    # Extract images from page
    for page in ocr_response.pages:
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        # Replace image placeholders with actual images
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))

    return "\n\n".join(markdowns)

# Combine OCR text and images into a single Markdown document
combined_markdown = get_combined_markdown(pdf_response)

# Save the Markdown content to a file
output_file = f'{pdf_file.stem}.md'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(combined_markdown)

print(f"Markdown content has been saved to: {output_file}")



