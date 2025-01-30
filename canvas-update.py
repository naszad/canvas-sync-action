import os
import sys
import mimetypes
from pathlib import Path
from canvasapi import Canvas

API_URL = os.getenv("CANVAS_API_URL")  # e.g. "https://<your-domain>.instructure.com"
API_KEY = os.getenv("CANVAS_API_KEY")  # Canvas Access Token (secret!)
COURSE_ID = os.getenv("CANVAS_COURSE_ID")  # e.g. "123456"
ROOT_LOCAL_PATH = os.getenv("LOCAL_REPO_PATH", ".")  # path to the cloned repo

if not API_URL or not API_KEY or not COURSE_ID:
    print("Missing required environment variables (CANVAS_API_URL, CANVAS_API_KEY, CANVAS_COURSE_ID).")
    sys.exit(1)

# Initialize Canvas
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

# Get or create a Canvas folder by name & parent_folder_id
def get_or_create_canvas_folder(folder_name, parent_folder):
    """
    Return a Canvas folder object with the given name under the parent_folder.
    If it doesn't exist, create it.
    """
    print(f"Attempting to create/get folder '{folder_name}' under parent '{parent_folder.name}'")
    
    # Check if folder already exists
    subfolders = parent_folder.get_folders()
    for sf in subfolders:
        if sf.name == folder_name:
            print(f"Found existing folder: {sf.name} (ID: {sf.id})")
            return sf  # found existing folder

    # If not found, create a new folder
    print(f"Creating new folder '{folder_name}'")
    new_folder = parent_folder.create_folder(name=folder_name)
    print(f"Created folder: {new_folder.name} (ID: {new_folder.id})")
    return new_folder

# Replicate a local directory to a Canvas folder
def replicate_directory_to_canvas(local_path, canvas_folder):
    """
    For each subdirectory in local_path, create/find a matching Canvas folder.
    For each file, upload it into the canvas_folder.
    """
    print(f"\nProcessing directory: {local_path}")
    print(f"Current Canvas folder: {canvas_folder.name} (ID: {canvas_folder.id})")
    
    for entry in os.scandir(local_path):
        if entry.is_dir():
            # Skip .git or other hidden folders
            if entry.name.startswith("."):
                continue
            print(f"\nProcessing subdirectory: {entry.name}")
            subfolder = get_or_create_canvas_folder(entry.name, canvas_folder)
            if subfolder.name != entry.name:
                print(f"WARNING: Created folder name mismatch! Expected: {entry.name}, Got: {subfolder.name}")
            replicate_directory_to_canvas(entry.path, subfolder)
        elif entry.is_file():
            # Skip hidden files or files that shouldn't be uploaded
            if entry.name.startswith("."):
                continue
            print(f"\nUploading file: {entry.name}")
            upload_file_to_canvas(entry.path, canvas_folder)

# Upload a single file to Canvas
def upload_file_to_canvas(local_file_path, canvas_folder):
    """
    Uploads a local file to the specified Canvas folder.
    If a file with the same name already exists in Canvas, it will be replaced.
    """
    file_name = os.path.basename(local_file_path)
    print(f"Uploading {file_name} to folder '{canvas_folder.name}' (ID: {canvas_folder.id})")

    # canvasapi Folder object has an .upload() method that handles the file upload
    try:
        status, response = canvas_folder.upload(local_file_path)
        print(f"Upload response - Status: {status}")
        print(f"Response details: {response}")
        
        if status != "ready":
            print(f"WARNING: Upload for {file_name} returned status '{status}'.")
        else:
            print(f"SUCCESS: {file_name} uploaded as {response['filename']} (ID {response['id']}).")
    except Exception as e:
        print(f"ERROR uploading {file_name}: {str(e)}")

# Utility: Get the root folder in a Canvas course
def get_root_folder(course):
    """
    Return the folder in the course whose 'parent_folder_id' is None.
    This is effectively the 'root' folder in Canvas.
    """
    folders = course.get_folders()
    for f in folders:
        if f.parent_folder_id is None:
            return f
    return None  # If none found, return None

# Main Execution
def main():
    # 1. Get the course's root folder
    root_canvas_folder = course.get_folders()
    course_root = None
    for folder in root_canvas_folder:
        if folder.full_name == "course files":
            course_root = folder
            break
    
    if not course_root:
        print("Could not find the course root folder!")
        sys.exit(1)

    github_folder_name = "GitHub_Replica"
    # Create or get our GitHub_Replica folder
    top_level_folder = get_or_create_canvas_folder(github_folder_name, course_root)

    # 2. Recursively replicate local repo directories & files into Canvas
    local_repo_path = Path(ROOT_LOCAL_PATH).resolve()
    print(f"Starting replication from {local_repo_path} to Canvas folder '{github_folder_name}'...")
    replicate_directory_to_canvas(str(local_repo_path), top_level_folder)
    print("Replication complete.")

if __name__ == "__main__":
    main()
