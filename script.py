# Needed for reading the CSV file
import csv

# Needed for handling file paths etc
import os

# Needed for copying files
import shutil

# Needed for checking command line arguments
import sys

# Check that there is exactly one argument provided to the script
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} path/to/file.csv')
    sys.exit(1)

# Check that the one argument provided to the script is a valid CSV file
file_name = sys.argv[1]
if not os.path.isfile(file_name) or not file_name.endswith('.csv'):
    print(f'Expected a csv file, but got {file_name}')

# This gets the absolute directory of the csv file
directory_containing_csv_file = os.path.dirname(os.path.realpath(file_name))

# Create an empty list of files to process that will be filled by reading the csv file
paths_to_files = []
file_names = []

# Read the CSV file
with open(file_name, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    # Skip the header row
    next(csv_reader)

    # Loop through all the remaining rows
    for line in csv_reader:

        # Get the third column of the line (e.g. "1970_July1970_July281970_Page01")
        file_identifier = line[2]

        # Split that string by the underscore character
        directory_parts = file_identifier.split('_')

        # The last part (index -1) is the name e.g. Page01
        file_names.append(directory_parts[-1])

        # Join all the paths together to give an absolute path to the files
        paths_to_files.append(os.path.join(directory_containing_csv_file, *directory_parts[:-1]))

# Create a directory for the files to be put into
directory_to_copy_into = os.path.join(directory_containing_csv_file, 'new_dir')
os.makedirs(directory_to_copy_into, exist_ok=True)

# Loop over all the paths & files we've extracted from the CSV file
for path, filename in zip(paths_to_files, file_names):

    # Warn if the directory isn't found
    if not os.path.isdir(path):
        print(f'Warning: {path} is not a valid directory')
        continue

    # To keep track of whether the file was successfully found and copied
    copied_file = False

    # Loop through all the files in the target directory
    for file in os.listdir(path):

        # If the file starts with the filename extracted from the CSV file, copy it
        if file.startswith(filename):

            # Get the full path to the file, including the file extension
            full_path_to_file = os.path.join(path, file)

            # Perform the file copy
            shutil.copy(full_path_to_file, directory_to_copy_into)

            # Mark that we have successfully copied it
            copied_file = True

            # Don't bother with the rest of this inner for loop: we have already found the file
            break

    # Print a warning if the file was not found in the directory
    if not copied_file:
        print(f'Warning: {path} did not include a file starting with {filename}')
