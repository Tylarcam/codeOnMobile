import os

def move_file_to_target(source_file_path, target_directory):
    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)

    # Define the target file path
    target_file_path = os.path.join(target_directory, os.path.basename(source_file_path))

    try:
        # Move the file
        os.rename(source_file_path, target_file_path)
        print(f"File moved to {target_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{source_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# List files in the current working directory with numbers
print("Files in the current directory:")
files = os.listdir('.')
for index, file in enumerate(files):
    print(f"{index + 1}: {file}")

# Prompt user for file selection by number
while True:
    try:
        selection = int(input("Enter the number of the file to move: "))
        if 1 <= selection <= len(files):
            source_file = files[selection - 1]
            break
        else:
            print(f"Please enter a number between 1 and {len(files)}")
    except ValueError:
        print("Please enter a valid number")

# Replace with your target directory path
target_directory = os.path.expanduser('~/Documents/AssemblyAI/audio')

# Move the selected file to the target directory
move_file_to_target(source_file, target_directory)