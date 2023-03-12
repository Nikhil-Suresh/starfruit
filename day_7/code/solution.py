import re

with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.


class Directory:
    """A class representing a directory."""
    
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.parent = parent

    def __repr__(self):
        return f"Directory: {self.name}"
    
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
    

class DiskFile:
    """A class representing a file."""
    
    def __init__(self, name, size, parent):
        self.name = name
        self.size = int(size)
        self.parent = parent
    
    def __repr__(self):
        return f"DiskFile: {self.name}, Size: {str(self.size)}"

# Matches -> Captures:
# $ cd / -> /
# $ cd nwh -> nwh
CD_MATCH = r"\$ cd (.*)"
DIRECTORY_MATCH = r"dir (\w+)"
FILE_MATCH = r"(\d+) (\w+\.?\w*)"

def parse_file(object, parent):
    """Parses a directory or file from a string."""
    
    file_match_object = re.match(FILE_MATCH, object)
    if file_match_object:
        file_size = file_match_object.group(1)
        file_name = file_match_object.group(2)
        return DiskFile(file_name, file_size, parent=parent)
    
current_directory = None
for row in raw_input:
    directory_change_object = re.match(CD_MATCH, row)
    if directory_change_object:
        # Create a new directory and set it as the current directory.
        directory_name = directory_change_object.group(1)
        if directory_name == '..': # Go up a directory.
            current_directory = current_directory.parent
        elif current_directory == None:
            current_directory = Directory(directory_name)
        else:
            new_directory = Directory(directory_name, parent=current_directory)
            current_directory.children.append(new_directory)
            current_directory = new_directory
    else:
        parsed_object = parse_file(row, parent=current_directory)
        if parsed_object:
            current_directory.children.append(parsed_object)

def find_root_directory(directory):
    """Finds the root directory of a directory."""
    if directory.parent == None:
        return directory
    else:
        return find_root_directory(directory.parent)
    
root_directory = find_root_directory(current_directory)

def get_all_directories(directory):
    """Returns a list of all directories in a directory."""
    directories = []
    for child in directory.children:
        if isinstance(child, Directory):
            directories.append(child)
            directories += get_all_directories(child)
    return directories

all_directories = get_all_directories(root_directory)

print("Part 1:")
directories_smaller_than_100000 = [directory for directory in all_directories if directory.total_size <= 100000]
print(f"Total size of directories smaller than 100000:")
print(sum(map(lambda directory: directory.total_size, directories_smaller_than_100000)))

#####
# PART 2
#####
print("\nPart 2:")
TOTAL_DISK_SPACE = 70000000
AVAILABLE_DISK_SPACE = TOTAL_DISK_SPACE - root_directory.total_size
DISK_SPACE_TO_FREE = 30000000 - AVAILABLE_DISK_SPACE

directories_large_enough_for_deletion = [directory for directory in all_directories if directory.total_size >= DISK_SPACE_TO_FREE]
smallest_directory = min(directories_large_enough_for_deletion, key=lambda directory: directory.total_size)
print(f"Smallest directory large enough to delete: {smallest_directory.name} with size {smallest_directory.total_size}.")