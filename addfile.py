import os
import shutil
import csv
import argparse

FILES_FOLDER = "files"
OUTPUT_CSV = "recap.csv"

# gets the extension of a file, returns None if there is no extension
def get_extension(filename):
    if filename.count(".") == 0:
        return None
    return filename.split(".")[-1]

# gets the type of file based on its extension
def get_type(filename):
    extension = get_extension(filename)
    if extension == "mp3":
        return "audio"
    if extension in ["odt", "txt"]:
        return "docs"
    if extension in ["jpg", "jpeg", "png"]:
        return "images"
    return None

# utility function to load the CSV file
def load_csv(filepath):
    data = []
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    return data

def move_file(filename):
    # read the csv file previous data
    csv_data = load_csv(OUTPUT_CSV)
    if len(csv_data) == 0:
        csv_data.append(["filename", "folder", "size"])

    # get file info and move it to the right folder
    folder = get_type(filename)
    try:
        size = os.path.getsize(f"{FILES_FOLDER}/{filename}")
    except FileNotFoundError:
        print(f"File {filename} not found")
    else:

        if folder is None:
            print(f"Failed to recognize {filename} extension")
        else:
            print(f"Moving {filename} of {size}B to {folder}")
            directory = f"{FILES_FOLDER}/{folder}"
            if not os.path.exists(directory):
                os.mkdir(directory)
            shutil.move(f"{directory}", f"{directory}/{filename}")
            csv_data.append([filename, folder, size])
        
        # write the csv file
        with open(OUTPUT_CSV, "w") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        print("Done!")

# ask for the filename and execute the move_file function
parser = argparse.ArgumentParser(description="Move files to the right folder")
parser.add_argument("filename", help="Name of the file to move")
args = parser.parse_args()
move_file(args.filename)
