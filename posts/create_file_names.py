import os

# Get the current directory
current_dir = os.getcwd()

# Specify the output file path
output_file_path = "file_names.txt"

# Open the output file in append mode
with open(output_file_path, 'a') as output_file:
    
    # Write the current directory name to the file
    output_file.write(f"Files in {current_dir}:\n")
    
    # Get a list of all files in the current directory and its subdirectories
    for foldername, subfolders, filenames in os.walk(current_dir):
        # Write the folder name to the file
        output_file.write(f"\nFolder: {foldername}\n")
        
        # Write the names of all files in the folder to the file
        for filename in filenames:
            output_file.write(filename + '\n')

print(f"File names have been appended to '{output_file_path}'.")
