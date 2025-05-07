# Project File Reader

### Project Description
This project is designed to read files from Google Drive, process them using OCR (Optical Character Recognition), and generate Markdown files for further use.

---

## Libraries
### Required Libraries
Below are the libraries used in this project, along with their installation commands and descriptions:

1. **Google API Client**
   ```bash
   pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
   ```
   - Used to interact with Google Drive for file uploads and downloads.

2. **OpenAI**
   ```bash
   pip install openai
   ```
   - Used for integrating OpenAI's GPT models for text processing.

3. **MistralAI**
   ```bash
   pip install mistralai
   ```
   - Used for OCR and document processing.

---

## Environment Variables
The following environment variables are required for the project to function correctly:

1. **`api_key`**
   - Purpose: API key for MistralAI to authenticate requests.

2. **`gdrive_link`**
   - Purpose: Link to the Google Drive folder containing the files to process.

3. **`folder_id`**
   - Purpose: The unique ID of the Google Drive folder.

4. **`service_file`**
   - Purpose: Path to the Google Service Account JSON file for authentication.

5. **`download_dir`**
   - Purpose: Directory where files downloaded from Google Drive will be stored.

6. **`markdown_dir`**
   - Purpose: Directory where the generated Markdown files will be saved.

7. **`open_api`**
   - Purpose: API key for OpenAI to authenticate requests.

---

## Functions
Below is a list of the key functions in the project and their descriptions:

1. **`var_dict()`**
   - Description: Creates a dictionary of global variables and their values.

2. **`update_variables(var_dict)`**
   - Description: Updates the global variables with new values provided by the user.

3. **`enter_variables(var)`**
   - Description: Prompts the user to enter or update variable values.

4. **`current_variables()`**
   - Description: Displays the current values of all variables.

5. **`user_interface()`**
   - Description: Provides a user-friendly interface to view and update variables.

6. **`client.files.upload()`**
   - Description: Uploads a local file to MistralAI for OCR processing.

7. **`client.files.get_signed_url()`**
   - Description: Retrieves a signed URL for accessing the uploaded file.

8. **`client.chat.complete()`**
   - Description: Sends a chat request to MistralAI or OpenAI and retrieves the response.

---

## Installation
### Google API
```bash
pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```

### OpenAI
```bash
pip install openai
```

### MistralAI
```bash
pip install mistralai
```

---

## Usage
1. Set up the required environment variables in your system or a `.env` file.
2. Run the script to process files from Google Drive and generate Markdown outputs.
3. Use the user interface to update or view the current configuration.
