import fitz  # PyMuPDF
import base64
from openai import OpenAI



def extract_images_from_pdf(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)
    return images

# Example usage
pdf_path = r"C:\Users\aiden\POCKETS\CODE\TEST DUMMY\G Drive Files\Grazed Foundation (Profile and Proposal).V1 02192025.pdf"
extracted_images = extract_images_from_pdf(pdf_path)


if extracted_images:
    # Convert the first extracted image to Base64
    base64_image = base64.b64encode(extracted_images[0]).decode("utf-8")
    
    # Use the Base64 image in your OpenAI API call
    client = OpenAI(api_key="Your_openai_key")

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "what's in this image?" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    print(response.output_text)
else:
    print("No images found in the PDF.")
