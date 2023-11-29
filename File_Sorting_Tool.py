import os
from tkinter import Tk, Button, filedialog
from PIL import Image
import PyPDF2
import shutil

# This function will convert all the jpeg files to PDFs and then sort them accordingly based on their naming convention.
# After all the files have been converted it will then merge all the PDF's together.
def run_program():
    
    directory = filedialog.askdirectory(title='Select Directory')

    files = {}

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        
        if not filename.lower().endswith(('.jpg', '.jpeg')):
            print(f"{filename} is not a JPEG image")
            continue

        # Split the file name into prefix and extension
        prefix, ext = os.path.splitext(filename)

        # Check if the file name contains a valid prefix and number
        if '(' in prefix and ')' in prefix:
            try:
                number = prefix[prefix.index('(') + 1: prefix.index(')')]
                prefix = prefix[:prefix.index('(')]
            except ValueError:
                print(f"{filename} does not contain a valid prefix and number")
                continue
        else:
            print(f"{filename} does not contain a valid prefix and number")
            continue

        if prefix not in files:
            files[prefix] = []

        files[prefix].append(filename)

    # Create a subdirectory for each prefix and move the files into it
    for prefix, filenames in files.items():
        
        os.makedirs(os.path.join(directory, prefix), exist_ok=True)

        # Convert the JPEG images to PDF and save them in the subdirectory
        pdf_files = []
        for filename in filenames:
            # Convert the JPEG image to PDF
            img = Image.open(os.path.join(directory, filename))
            pdf_filename = f"{os.path.splitext(filename)[0]}.pdf"
            pdf_path = os.path.join(directory, prefix, pdf_filename)
            img.save(pdf_path, "PDF", resolution=100.0)
            pdf_files.append(pdf_path)

        # Combine the PDF files into a single PDF
        output_pdf_path = os.path.join(directory, prefix, f"{prefix}.pdf")
        merge_pdfs(pdf_files, output_pdf_path)

        # Remove the individual PDF files
        for pdf_file in pdf_files:
            os.remove(pdf_file)


# Takes the functionality of the file mover, but converts all the jpeg files into PDFS
# Also creates folders for the naming of the files and sorts them accordingly.
def pdf_convert():
    # Get the directory where the files are stored
    directory = filedialog.askdirectory(title='Select Directory')

    
    files = {}

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        
        if not filename.endswith('.jpg') and not filename.endswith('.jpeg'):
            print(f"{filename} is not a JPEG image")
            continue

        prefix, ext = os.path.splitext(filename)

        if '(' in prefix and ')' in prefix:
            try:
                number = prefix[prefix.index('(') + 1: prefix.index(')')]
                prefix = prefix[:prefix.index('(')]
            except ValueError:
                print(f"{filename} does not contain a valid prefix and number")
                continue
        else:
            print(f"{filename} does not contain a valid prefix and number")
            continue

        # If the prefix is not already in the dictionary, add it
        if prefix not in files:
            files[prefix] = []

        files[prefix].append(filename)

    # Create a subdirectory for each prefix and move the files into it
    for prefix, filenames in files.items():
        os.makedirs(os.path.join(directory, prefix), exist_ok=True)

        for filename in filenames:
            # Convert the JPEG image to PDF
            img = Image.open(os.path.join(directory, filename))
            pdf_filename = f"{os.path.splitext(filename)[0]}.pdf"
            pdf_path = os.path.join(directory, prefix, pdf_filename)
            img.save(pdf_path, "PDF", resolution=100.0)

            # Move the PDF file into the subdirectory
            src = pdf_path
            dst = os.path.join(directory, prefix, pdf_filename)
            shutil.move(src, dst)


#Selects a directory folder then sorts all jpeg files into a folder named accordingly after the file name. 
def file_mover():
    directory = filedialog.askdirectory(title='Select Directory')
    files = {}

    for filename in os.listdir(directory):

        # check if the file name contains an underscore character
        if '_' not in filename:
            continue

        parts = filename.rsplit('_', 1)
        if len(parts) != 2:
            continue
        prefix, number = parts

        if prefix not in files:
            files[prefix] = []

        files[prefix].append(filename)

    # create a subdirectory for each prefix and move the files into it
    for prefix, filenames in files.items():

        os.mkdir(os.path.join(directory, prefix))

        for filename in filenames:
            src = os.path.join(directory, filename)
            dst = os.path.join(directory, prefix, filename)
            shutil.move(src, dst)


# merges multiple PDF files into a single PDF
def merge_pdfs(input_files, output_file):
    merger = PyPDF2.PdfMerger()

    for input_file in input_files:
        merger.append(input_file)

    merger.write(output_file)
    merger.close()


# Create the main window
root = Tk()
root.title("File Sorter")

# Function to handle calling functions from onclick
def on_button_click():
    run_program()
    print("Program completed successfully!")

def on_button_click2():
    pdf_convert()
    print("Program completed successfully!")

def on_button_click3():
    file_mover()
    print("Program Completed successfully!")

# Creates a button widget for each function
button = Button(root, text="Merge Files", command=on_button_click, width=40, height=8)
button.pack()

convert_button = Button(root, text="Convert To PDF", command=on_button_click2, width=40, height=8)
convert_button.pack()

file_mover_button = Button(root, text="Sort Into Folder", command=on_button_click3, width=40, height=8)
file_mover_button.pack()

root.mainloop()