import os

a = "314aabc"
b = a
serial = "12345"
parent = "engine transmission"

# Create the directory structure if it doesn't exist
directory_path = os.path.join(".", serial, parent)
os.makedirs(directory_path, exist_ok=True)

# Create the file in the specified directory
file_path = os.path.join(directory_path, f"{b}.txt")
f = open(file_path, "w")