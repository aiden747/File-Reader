# Project Outline
The goal of this project is to take in different file types from a google drive, upload the file data, access file data later and manipulate files and file data

## Project Idea:
- Download files from Google Drive
- Read the Data of Google Drive files regardless of file type
- Upload Google Drive file Data to storage
- Manipulate files and Access file Data


## TODO:
1. Access the files in a Google Drive
2. Download the files off the Google Drive
3. Read the data off the downloaded files
    - File type
4. Upload and store the file data
    - Markdown String
5. Access individual file data
6. Manipulate files and the file data



## Google Drive TODO:
- ~~Get Google Drive folder link~~
- ~~Get Google Drive folder ID~~
- ~~Create a Directory to store the downloaded files~~
- ~~Access Google Drive files using Google Drive API~~
- ~~Download the files from Google Drive into a Download Directory~~


## Google Drive Download Structure:

### Google Drive API Install:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

### Imports:
- `import os`
- `from google.oauth2 import service_account`
- `from googleapiclient.discovery import build`
- `import io`
- `from googleapiclient.http import MediaIoBaseDownload`

---

### Class Variables
- self.link
- self.link_id
- self.download_directory
- self.json_file
- self.scope
- self.files

---

### Class Functions
- get_all_variables(self)
    - this Function returned all the class variables as a single tuple
- print_all_variables(self)
    - This Function printed and formated the 6 class variables to make reading all the variables easier
- print_files(self)
    - Prints the name of every file that was downloaded, using a for loop and the file data
- get_link_id(self)
    - Finds and returns the Folder ID by extracting it from the Google Drive link
- scope_access(self)
    - Provides an easy and efficent way to change the Google Drives API Access Scope
- update_variable(self)
    - Takes in user inputs to chose one of the 6 class variables and give it a new value
- download_files(self)
    - Downloads all the files from a Google Drive Folder into a designated directory and stores all the files metadata

---

### Functions
- access_practice_folder()
    - Used as a template and reference on how it works, easy to understand because of the static google drive variables
- main()
    - This function will loop the code so it keeps running until i tell it to end

---

### Variables:
**Google Drive Folder Link:**
- https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link

**Google Drive Folder ID**
- 16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft

**Download Directory**
- `C:\Users\aiden\Personal\Project File-Upload\Google Drive`

**JSON Credentials File Path**
- `C:\Users\aiden\Personal\Project File-Upload\file-reader-456206-7659069c7d5d.json`

**API Access Scope**
- ```[https://www.googleapis.com/auth/drive]``` - Full access 
- ```[https://www.googleapis.com/auth/drive.readonly]``` - Read-only access
- ```[https://www.googleapis.com/auth/drive.file]``` - Access to files created/opened by app: 


---

## google_drive.py USE:
- Downloads the files from the google drive and store the file data
- Any files that return an error are added to a different directory
- Stores the Google Drive link and JSON file path
- Will store the directory path for the downloads and failed downloads
- Mainly tasked to store the file data of all downloaded files

---

## File Download Reference
```
## This code opens a practice Google Drive and downloads it into a designated folder

import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


# This is the link to the Google Drive folder
link = 'https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link'

# This is the ID of the Google Drive folder
link_id = '16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft'

# Creates a Download Directory for the Google Drive files, if one does not exist
download_directory = r'C:\Users\aiden\Personal\Project File-Upload\Google Drive' 
os.makedirs(download_directory, exist_ok=True)  

# Ths is the path to the JSON file that contains the account credentials for the Google Drive API
json_file = r'C:\Users\aiden\Personal\Project File-Upload\file-reader-456206-7659069c7d5d.json'

# This is the scope of access for the Google Drive API
scope = ['https://www.googleapis.com/auth/drive']

# The service account JSON file is used to authenticate the API requests
credentials = service_account.Credentials.from_service_account_file(json_file, scopes=scope)
drive_service = build('drive', 'v3', credentials=credentials)
query = f"'{link_id}' in parents and trashed = false"

# The query is used to list the files in the Google Drive folder
results = drive_service.files().list(q=query, fields="files(id, name)").execute()
files = results.get('files', [])

# Downloads the files from the Google Drive folder into the Download Directory
for file in files:
    
    # Gets the file metadata and creates a file path
    file_path = os.path.join(download_directory, file['name'])
    request = drive_service.files().get_media(fileId=file['id'])
    fh = io.FileIO(file_path, 'wb')

    # Downloads the file in chunks and saves it to the created file path
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    # This loop will download the file in chunks until it is complete
    while not done:
        status, done = downloader.next_chunk()

    # Prints the status of the download
    print(f"[{file['name']} Downloading...]")

# Prints when the download is done
print("[Finished Download]")

```

## google_drive.py Code

```

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

# Class to store variables to access Google Drive and files
class GoogleDriveDownLoader:

    # Constructor to initialize the class variables
    def __init__(self, link='https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link', link_id='16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft', download_directory=r'C:\Users\aiden\Personal\Project File-Upload\Google Drive', json_file=r'C:\Users\aiden\Personal\Project File-Upload\file-reader-456206-7659069c7d5d.json', scope=['https://www.googleapis.com/auth/drive'], files=None):

        # Google Drive Folder Link
        self.link = link
        # Google Drive Folder ID
        self.link_id = link_id
        # Google Drive File Download Directory
        self.download_directory = download_directory
        # JSON file path for Google Drive API credentials
        self.json_file = json_file
        # Google Drive API Access Scope
        self.scope = scope
        # Downloaded Google Drive Files
        self.files = files

    
    # Returns all the Class variables as a tuple
    def get_all_variables(self):
        return self.link, self.link_id, self.download_directory, self.json_file, self.scope, self.files


    # Prints all the Class variables
    def print_all_variables(self):

        # Prints what the variable is, then prints whats stored
        print(f"Google Drive Folder Link: \n- {self.link}\n")
        print(f"Google Drive Folder ID: \n- {self.link_id}\n")
        print(f"File Download Directory: \n- {self.download_directory}\n")
        print(f"JSON File Path: \n- {self.json_file}\n")
        print(f"Google Drive API Access Scope: \n- {self.scope}\n")
        print("Google Drive Files Downloaded:")

        # If the files variable exists, prints every file name
        if self.files:
            for file in self.files:
                print(f"- {file['name']}")
            print()
        else:
            print("None\n")


    # Loops through downloaded file list and prints them
    def print_files(self):

        # Prints each item in the files list using a for loop
        print("Here are the downloaded files:")
        for file in self.files:
            print(f"{file['name']}...")


    # Gets the Folder ID from the Google Drive Link
    def get_link_id(self):
        self.link_id = self.link.split(r'folders/')[1].split('?')[0]


    # Can change the Google Drive API access scope by selecting one of the tree choices
    def scope_access(self):
        user = input("Please enter the corresponding number for the scope of access you would like:\n1.) Full Access\n2.) Read-Only Access\n3.) Access to files created/opened by app:\n")
        
        # Reassigns the variable based on the users input
        if user == '1':
            self.scope = ['https://www.googleapis.com/auth/drive']
            print("Full Access granted.")
        elif user == '2':
            self.scope = ['https://www.googleapis.com/auth/drive.readonly']
            print("Read-Only Access granted.")
        elif user == '3':
            self.scope = ['https://www.googleapis.com/auth/drive.file']
            print("Access to files created/opened by app granted.")
        else:
            print("Invalid input. Variable set to 'None'.")
            self.scope = None
        
        return
        

    # The user selects a variable, the value of that variable can be changed by the user, the variable is updated and then stored in the class variable
    def update_variable(self):
        
        # The user is prompted to select a variable to update
        var_num = input("Enter the corrosponding number for the variable you would like to update:\n1. Google Drive Link\n2. Google Drive Folder ID\n3. Download Directory\n4. JSON File Path\n5. Google Drive API Scope\n6. File List\n7. None\n")
        
        # Updates a variables value with the new user input
        if var_num == '1':
            self.link = input(f"Please enter a new value for {self.link}:\n")
        elif var_num == '2':
            self.link_id = input(f"Please enter a new value for {self.link_id}:\n")
        elif var_num == '3':
            self.download_directory = input(f"Please enter a new value for {self.download_directory}:\n")
        elif var_num == '4':
            self.json_file = input(f"Please enter a new value for {self.json_file}:\n")
        elif var_num == '5':
            self.scope = input(f"Please enter a new value for {self.scope}:\n")
        elif var_num == '6':
            self.files = input(f"Please enter a new value for {self.files}:\n")
        elif var_num == '7':
            print("Variables remain unchanged.")
        else:
            print("Invalid input. Variable is unchanged.")

        return


    # Downloads the files from the Google Drive Folder into a Directory and stores the file metadata in the class variable 'files'
    def download_files(self, link_id=None, download_directory=None, json_file=None, scope=None):
        
        # If no value was passed into the parameters, the class variables are used instead
        link_id = link_id if link_id is not None else self.link_id
        download_directory = download_directory if download_directory is not None else self.download_directory
        json_file = json_file if json_file is not None else self.json_file
        scope = scope if scope is not None else self.scope

        # Creats the Download Directory for the Google Drive Files if one doesnt already exist
        os.makedirs(download_directory, exist_ok=True)

        credentials = service_account.Credentials.from_service_account_file(json_file, scopes=scope)
        drive_service = build('drive', 'v3', credentials=credentials)
        query = f"'{link_id}' in parents and trashed = false"

        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])    

        # Prints the start of download
        print("Download Started")

        # Downloads each file from the Google Drive Folder into the Download Directory
        for file in files:
            
            file_path = os.path.join(download_directory, file['name'])
            request = drive_service.files().get_media(fileId=file['id'])
            fh = io.FileIO(file_path, 'wb')
            
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()
                # Prints the status of the download
                print(f"Downloading {file['name']}...")

        #Prints the end of the Download
        print("Download Finished")
        print('END\n')
        
        # returns the downloaded files data instead of assigning it to a class variable
        return files



# Uses the practice variables to demonstrate how it works, and for a reference
def access_practice_folder():

    # This is the link to the Google Drive folder
    link = 'https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link'
    # This is the ID of the Google Drive folder
    link_id = '16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft'

    # Creates a Download Directory for the Google Drive files, if one does not exist
    download_directory = r'C:\Users\aiden\Personal\Project File-Upload\Google Drive' 
    os.makedirs(download_directory, exist_ok=True)  

    # Ths is the path to the JSON file that contains the account credentials for the Google Drive API
    json_file = r'C:\Users\aiden\Personal\Project File-Upload\file-reader-456206-7659069c7d5d.json'

    # This is the scope of access for the Google Drive API
    scope = ['https://www.googleapis.com/auth/drive']

    # The service account JSON file is used to authenticate the API requests
    credentials = service_account.Credentials.from_service_account_file(json_file, scopes=scope)
    drive_service = build('drive', 'v3', credentials=credentials)
    query = f"'{link_id}' in parents and trashed = false"

    # The query is used to list the files in the Google Drive folder
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    # Downloads the files from the Google Drive folder into the Download Directory
    for file in files:
        
        # Gets the file metadata and creates a file path
        file_path = os.path.join(download_directory, file['name'])
        request = drive_service.files().get_media(fileId=file['id'])
        fh = io.FileIO(file_path, 'wb')

        # Downloads the file in chunks and saves it to the created file path
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        # This loop will download the file in chunks until it is complete
        while not done:
            status, done = downloader.next_chunk()

        # Prints the status of the download
        print(f"[{file['name']} Downloading...]")

    print("[Finished Download]")



if __name__ == "__main__":

    ## PRACTICE VARIABLES ##

    # The Practice variables stored for later use
    p_link = 'https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link'
    p_link_id = '16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft'
    p_download_directory = r'C:\Users\aiden\Personal\Project File-Upload\Google Drive'
    p_json_file = r'C:\Users\aiden\Personal\Project File-Upload\file-reader-456206-7659069c7d5d.json'
    p_scope = ['https://www.googleapis.com/auth/drive']
    p_files = [{'id': '1K7nvdgAEBBGZAP8QrcL1BZ-PJ_z6M7Os', 'name': 'parking-violation.png'}, {'id': '1pfunYGPwnkbGPHM13VVgXpQOsRak6W9G', 'name': '25MYUS_Ford_F150_WTY_V5.pdf'}, {'id': '1s_CpE3TB2DxytL_OxpORDZeC_xiTFpG7', 'name': 'receipt.png'}, {'id': '1FdC6jSJJgm3UL7z-e-syepmVGW4vfdlB', 'name': 'Grazed Foundation (Profile and Proposal).V1 02192025.pdf'}, {'id': '1nmvjsco2TqUhuDYNzClt_aEDuCX869lB', 'name': 'Invoice_2251071_from_FIBERLINK_CORP.pdf'}, {'id': '1tsQOEB7QayFSAoha2-MK80M_SD1uAnf6', 'name': 'History through Film - SEC_801 Syllabus.pdf'}]

    # Creates a Class object with the practice variables
    default = GoogleDriveDownLoader(p_link, p_link_id, p_download_directory, p_json_file, p_scope, p_files)

    # Prints all the practice Class variables
    default.print_all_variables()

    # Downloads the Files from the Google Drive Folder and assigns the File data to the Class File variable
    # files = default.download_files()

    # Creates practice values as regular variables
    link, id, directory, json, scope, files = default.get_all_variables()


    ## NEW CLASS OBJECT ##

    # Creates a new Class object
    #user = GoogleDriveDownLoader()

    # Downloads Files and stores them
    user_files = user.download_files()

    # Uploading File data to class
    user.self.files = user_files

    # Display Class Variables
    user.print_all_variables()


```
