import re

with open(r'..\input\test_input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

class Directory:
    """A class representing a directory."""
    
    def __init__(self, name, depth):
        self.name = name
        self.depth = depth
        self.children = []
        self.parsed = False

    def __repr__(self):
        return f"Directory: {self.name}, Depth: {self.depth}"
    
    @property
    def total_size(self):
        """Returns the total size of the directory and all its children."""
        total_size = 0
        for child in self.children:
            if isinstance(child, DiskFile):
                total_size += child.size
            if isinstance(child, Directory):
                total_size += child.total_size
        return total_size
    
    @property
    def direct_children(self):
        """Returns the number of direct children of the directory."""
        return [child for child in self.children if isinstance(child, DiskFile) and child.depth == self.depth + 2]

class DiskFile:
    """A class representing a file."""
    
    def __init__(self, name, size, depth,):
        self.name = name
        self.size = int(size)
        self.depth = depth
    
    def __repr__(self):
        return f"DiskFile: {self.name}, Size: {str(self.size)}, Depth: {self.depth}"

# Matches the following lines:
# - / (dir)
#     - e (dir)
# Note that the number of spaces at the start of the line is captured, alongside the name.
DIRECTORY_MATCH = re.compile(r'(\s*)-\s([/|\w+]\.?\w*)\s\(dir\)')

# Matches the following lines:
# - i (file, size=584)
#     - h.lst (file, size=62596)
# Note that the number of spaces at the start of the line is captured, alongside the name and file size.
# Also able to handle files with extensions.
FILE_MATCH = re.compile(r'(\s*)-\s([/|\w+]\.?\w*)\s\(file, size=(\d+)\)')

directories_and_files = []

for row in raw_input:
    # Check if the line is a directory or a file.
    directory_match = re.match(DIRECTORY_MATCH, row)
    diskfile_match = re.match(FILE_MATCH, row)
    if directory_match:
        # If it's a directory, create a Directory object and append it to the list.
        directory_name = directory_match.groups()[1] # The name of the directory.
        directory_depth = len(directory_match.groups()[0]) # The number of spaces at the start of the line.
        directories_and_files.append(Directory(directory_name, directory_depth))
    elif diskfile_match:
        # If it's a file, create a DiskFile object and append it to the list.
        diskfile_name = diskfile_match.groups()[1] # The name of the file.
        diskfile_depth = len(diskfile_match.groups()[0]) # The number of spaces at the start of the line.
        diskfile_size = diskfile_match.groups()[2] # The size of the file.
        directories_and_files.append(DiskFile(diskfile_name, diskfile_size, diskfile_depth))

def parse_folder_structure(directories_and_files, parent_depth=0):
    """A recursive function that parses a list of directories and files and 
    adds them to their parent directories.
    
    Some things to note:
    1. The list of directories and files is passed by reference, so any changes made to the list will be reflected in the original list.
    2. Each directory might be looped over multiple times, but this is fine because the function will only parse the directory if it hasn't been parsed before due to the 'parsed' attribute.
    """
    children = []
    for item in directories_and_files:
        if item.depth == parent_depth + 2 or item.name == '/': # '/' is the root directory and should be parsed regardless of its depth.
            # Parse directories if they haven't been parsed before.
            if isinstance(item, Directory) and item.parsed is False:
                # If the item is a directory, find its children.
                children.append(item) # Add the directory to the list of children, which will be returned.
                item.children += parse_folder_structure(directories_and_files[directories_and_files.index(item) + 1:], parent_depth=item.depth)
                item.parsed = True
            if isinstance(item, DiskFile):
                # If the item is a file, find its children.
                children.append(item)
    return children


parse_folder_structure(directories_and_files)

print(directories_and_files[1])
print(directories_and_files[1].total_size)

