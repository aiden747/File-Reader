# File Reader
#### Using Mistral OCR API
<br>

## PDF

### `pdf_extractor.py`
- The **main** file to extract data from a PDF file.
- Extracts the text and image data from the PDF file using the **Mistral OCR API**.
- Combines the extracted data into a single string then saves that string into a Markdown file.
- Intended to be the **template module** for PDF extraction.
- Is fully **self-contained**.

  
### `pdf_reference.py`
- Contains code from the **OCR documentation**.
- Primarily used for refernece and understanding how the code actually works.
- A little clunkier and slower than the **`pdf_extractor.py`**.
- Essentially completes the same task as **`pdf_extractor.py`**.


###  `pdf_notebook.ipynb`
- Formats the **`pdf_extractor.py`** into smaller cells.
- Accomplishing tasks like data analysis, debugging, and prototyping is made easier.
- Cells provide the ability to run code in small chuncks, get immediate feedback, easier visualization, and Error isolation


### `pdf_notebook_reference.ipynb` (WIP)
- Formats the **`pdf_reference.py`** into smaller cells.
- Accomplishing tasks like data analysis, debugging, and prototyping is made easier.
- Cells provide the ability to run code in small chuncks, get immediate feedback, easier visualization, and Error isolation

<br><br><br>

## PNG

### `png_extractor.py` (WIP)
- The **main** file used to extract data from a PNG file.
- Extracts the text data from a PNG file using **Mistral OCR API**.
- Outputs the extracted data as a dictionary.
- Intended to be the **template module** for PNG extraction.
- Fully **self-contained script**.
- WIP


### `png_reference_1.py` (WIP)
- Contains the first part of code from the **OCR documentation**.
- Extracts PNG data and outputs it.
- WIP


### `png_reference_2.py` (WIP)
- Contains the second part of code from the **OCR documentation**.
- Extracts PNG data and outputs it.
- WIP


### `png_notebook.ipynb` (WIP)
- Formats the code from **`png_extractor.py`** into cells.
- Accomplishing tasks like data analysis, debugging, and prototyping is made easier.
- Cells provide the ability to run code in small chuncks, get immediate feedback, easier visualization, and Error isolation.


### `png_notebook_reference_1.ipynb` (WIP)
- Formats the code from **`png_reference_1.py`** into cells.
- Accomplishing tasks like data analysis, debugging, and prototyping is made easier.
- Cells provide the ability to run code in small chuncks, get immediate feedback, easier visualization, and Error isolation.


### `png_notebook_reference_2.ipynb` (WIP)
- Formats the code from **`png_reference_2.py`** into cells.
- Accomplishing tasks like data analysis, debugging, and prototyping is made easier.
- Cells provide the ability to run code in small chuncks, get immediate feedback, easier visualization, and Error isolation.


