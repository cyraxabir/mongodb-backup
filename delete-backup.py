import os
import glob

# Path to the backup folder
backup_folder = "/root/mongo-backup/"

# Get all JSON files in the folder
backup_files = glob.glob(os.path.join(backup_folder, "*.json"))

# Check if files are found
if not backup_files:
    print("No JSON files found in the directory.")
    exit()

# Sort files by modification time (newest first)
backup_files.sort(key=os.path.getmtime, reverse=True)

# Print all files sorted (for debugging)
print("Sorted files by modification time:")
for file in backup_files:
    print(file)

# Keep only the latest 4 files, delete the rest
files_to_delete = backup_files[3:]

# Debugging: Print files that will be deleted
print("Files to be deleted:")
if not files_to_delete:
    print("No files to delete.")
else:
    for file in files_to_delete:
        print(file)

# Attempt to delete the files
for file in files_to_delete:
    try:
        os.remove(file)
        print(f"Deleted: {file}")
    except Exception as e:
        print(f"Error deleting {file}: {e}")