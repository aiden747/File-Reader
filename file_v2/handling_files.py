import os
from extract_pdf import pdf_to_markdown


download_dir = r'C:\Users\aiden\Personal\Project File-Upload\Google Drive'

for file in os.listdir(download_dir):
    path = os.path.abspath(file)
    name, ext = os.splitext(file)
    if ext == '.pdf':
        pdf_to_markdown(path)







'''
def main():
    download_dir = get_config('DirectoryPaths', 'download')
    markdown_dir = get_config('DirectoryPaths', 'markdown')
    print(download_dir, markdown_dir)
    os.makedirs(markdown_dir, exist_ok=True)

    sort_file(download_dir)

#md_list = []

def sort_files(download_dir):    
    for file in os.listdir(download_dir):
        path = os.path.join(download_dir, file)
        name, ext = os.path.splitext(file)
        if ext == '.pdf':
            markdown = pdf_to_markdown(path)
            upload_markdown(markdown)
        elif ext == '.png':
            markdown = png_main(path)

def sort_file(download_dir):
    markdown_dir = get_config('DirectoryPaths', 'markdown')
    for file in os.listdir(download_dir):
        path = os.path.join(download_dir, file)
        name, ext = os.path.splitext(file)
        if ext == '.pdf':
            markdown = pdf_to_markdown(path)
            # Write markdown to a new file
            md_path = os.path.join(markdown_dir, f"{name}.md")
            with open(md_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown)
            print(f"Markdown file created: {md_path}")
            # If you have an upload function, call it here
            # upload_markdown(md_path)
        elif ext == '.png':
            markdown = png_main(path)
            md_path = os.path.join(markdown_dir, f"{name}.md")
            with open(md_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown)
            print(f"Markdown file created: {md_path}")
            # upload_markdown(md_path)

# Create the markdown files
#def create_files(markdown_string, path):
    # os.makedirs(markdown_dir, exist_ok=True)
    #pass

    
if __name__ == '__main__':
    #dir = get_config('DirectoryPaths', 'download')
    #print(dir)
    main()'''
