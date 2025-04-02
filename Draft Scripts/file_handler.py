from mistralai import Mistral
import os



'''
This module is to demonstrate and practice basic file handling in python.
    - Takes the name of a file and verifies that it exists in the current directory
    - Allows the user to access various information about the specified file
    - Displays file name
    - Displays absolute path of the file
    - Displays contents of the file based on the number of bytes specified to read by the user
'''

def main():
    # Get file name and verify it exists in the current directory
    file = get_file()

    # Ends the process if file doesnt exist
    if file == None:
        return
    
    # Displays any file information specified by the user
    if input('Would you like to access the file data? (yes/no)\n').strip().lower() == 'yes':
        retreive_data(file)
    
    

# Gets the file name and verifies it
def get_file():
    file_name = input('Enter the name of the PDF file to upload\n')

    # Check if the file exists in the current directory
    if os.path.exists(file_name):
        print(f'\nThe file [{file_name}] exists in the current directory.\n')
        return file_name
        
    else:
        print(f'\nError: The file {file_name} does not exist in the current directory.')
        # Prompt user for a different file name
        if input('Do you wish to enter another file name? (yes/no)\n').strip().lower() == 'yes':
            return get_file()
        else:
            return None




# Function to retrieve data from the file based on user input
def retreive_data(file):
    data = input('\nWhat data would you like to access? (file name/absolute path/contents/exit)\n')
    
    # Gets the name of the file
    if data == 'file name':
        # Get the file name of the file
        print(f'\nThe name of the file is:\n{file}\n')
        retreive_data(file)

    # Gets the absolute path of the file
    elif data == 'absolute path':
        # Get the absolute path of the file
        absolute_path = os.path.abspath(file)
        print(f'\nThe absolute path of the file is:\n{absolute_path}\n')
        retreive_data(file)

    # Gets the contents of the file based on user input for bytes
    elif data == 'contents':
        bytes = int(input('\nHow many bytes of data would you like to read?\n'))

        # Opens file in binary mode and reads the specified number of bytes
        with open(file, 'rb') as f:
            # Reads the specified number of bytes from the file
            content = f.read(int(bytes))
            print(f'\nThe contents of the file is:\n{content}\n')
            retreive_data(file)

    # End the data retrieval process if user types 'exit'
    elif data == 'exit':
        print('\nExiting data retrieval...\n')
        return
    
    # Invalid input handling
    else:
        print('\nError: Invalid input.\n')
        retreive_data(file)



if __name__ == "__main__":
    print('Running test.py...\n')
    main()
    print('\nDONE!')
