# File Reader
#### Using Mistral OCR API

## PDF

### `pdf_.py`
- Extracts the text and image data from the PDF file using the Mistral OCR API
- Combines the extracted data into one string in Markdown format and saves it as a Markdown file.
- Acts as a template module for future code.
- Is fully self-contained.
  
### `PDF_documentation.py`
- Contains the code from the OCR documentation.
- Mainly used to better understand how the code works.
- A clunkier slower version of PDF.py
- Accomplishes the same task as `PDF.py`.
  
###  `PDF_notebook.ipynb`
- Is the same as `PDF.py` but formated in Jupyter notebook.
- Splits the code into small cells.
- Code thats formated in cells can make prototyping faster, debugging easier, and provide better visualization.


## PNG

### `PNG.py`
- Extracts the text data from a PNG file using Mistral OCR API.
- Outputs the extracted data as a dictionary
- working on polishing up the code and understanding it

### `PNG_documentation_1.py`
- Contains part 1 of the code from the OCR documentation
- Extracts PNG data and outputs it
- Currently trying to understand how the code works

### `PNG_documentation_2.py`
- Contains part 2 of the code from the OCR documentation
- Extracts PNG data and outputs it
- Currently trying to understand how the code works
  
### `PNG_notebook_1.ipynb`
- contains the code from documentation part 1
- Formats code into cells to better understand each part of code individually
- Provides better understanding of how each part of the code works

### `PNG_notebook_2.ipynb`
- contains the code from documentation part 2
- Formats code into cells to better understand each part of code individually
- Provides better understanding of how each part of the code works
