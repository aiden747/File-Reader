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

    
    # Returns the Class variables as a tuple
    def get_all_variables(self):
        return self.link, self.link_id, self.download_directory, self.json_file, self.scope, self.files


    # Prints each file in the file list
    def print_files(self):
        print("Here are the downloaded files:")
        for file in self.files:
            print(f"{file['name']}...")


    # Gets the Folder ID from the Google Drive Link
    def get_link_id(self):
        self.link_id = self.link.split(r'folders/')[1].split('?')[0]


    # Can change the Google Drives API access scope by selecting one of the tree choices
    def scope_access(self):
        user = input("Please enter the corresponding number for the scope of access you would like:\n1.) Full Access\n2.) Read-Only Access\n3.) Access to files created/opened by app:\n")
        
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
            print("Invalid input. Variables remain unchanged.")

        return


    # Prints the Class variables
    def print_all_variables(self):
        print(f"Google Drive Folder Link: \n- {self.link}\n")
        print(f"Google Drive Folder ID: \n- {self.link_id}\n")
        print(f"File Download Directory: \n- {self.download_directory}\n")
        print(f"JSON File Path: \n- {self.json_file}\n")
        print(f"Google Drive API Access Scope: \n- {self.scope}\n")
        print("Google Drive Files Downloaded:")
        if self.files:
            for file in self.files:
                print(f"- {file['name']}")
            print()
        else:
            print("None\n")


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
        
        # Assigns the downloaded files to the class variable 'files'
        self.files = files
        return files



# Downloaded all the drive files into the directory
def drive_download(link, id, dir, json, scope):
    drive_class = GoogleDriveDownLoader(link, id, dir, json, scope)
    files = drive_class.download_files()
    drive_class.print_all_variables()
    return files






# Downloads the practice files from the Google Drive folder into a directory
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


# Provides a reference to the Google Drive folders using the practice variables
def reference_variables():

    # Variables
    link = 'https://drive.google.com/drive/folders/16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft?usp=drive_link'
    link_id = '16l1tmNrOmsM8IrFeZGl_YfsAwejuNmft'
    download_directory = r'C:\Users\aiden\Personal\Project File-Upload\Google Drive'
    json_file = r'C:\Users\aiden\Personal\Project File-Upload\file-reader-456206-7659069c7d5d.json'
    scope = ['https://www.googleapis.com/auth/drive']
    files = [{'id': '1K7nvdgAEBBGZAP8QrcL1BZ-PJ_z6M7Os', 'name': 'parking-violation.png'}, {'id': '1pfunYGPwnkbGPHM13VVgXpQOsRak6W9G', 'name': '25MYUS_Ford_F150_WTY_V5.pdf'}, {'id': '1s_CpE3TB2DxytL_OxpORDZeC_xiTFpG7', 'name': 'receipt.png'}, {'id': '1FdC6jSJJgm3UL7z-e-syepmVGW4vfdlB', 'name': 'Grazed Foundation (Profile and Proposal).V1 02192025.pdf'}, {'id': '1nmvjsco2TqUhuDYNzClt_aEDuCX869lB', 'name': 'Invoice_2251071_from_FIBERLINK_CORP.pdf'}, {'id': '1tsQOEB7QayFSAoha2-MK80M_SD1uAnf6', 'name': 'History through Film - SEC_801 Syllabus.pdf'}]

    # Class object
    reference_class = GoogleDriveDownLoader(link, link_id, download_directory, json_file, scope, files)

    # File variables
    link, id, dir, json, scope, files = reference_class.get_all_variables()
    vars = [link, id, dir, json, scope, files]

    return vars





