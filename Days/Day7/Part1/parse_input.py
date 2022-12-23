import re
from .data_structures import File, Directory


def is_command(potential_command: str) -> bool:
    """
    Check if a string is considered a command.

    Checks for a '$' to start the string, a space, then a cd or ls
     command, then an optional directory after the command.
    Format: '$ cd/ls opt(directory)'

    :param potential_command: The string to check.
    :return: True if the string is a command, False otherwise.
    """
    regex_cmd = r'^\$\s(cd|ls)(\s[a-zA-Z/\.]*)?$'
    return bool(re.search(regex_cmd, potential_command))


def is_file(potential_file: str) -> bool:
    """Check if a string is considered a file."""
    regex_file = r'^[0]*[1-9]+\d*\s[a-zA-Z]+(\.[a-zA-Z]{3})?$'
    return bool(re.search(regex_file, potential_file))


def is_directory(potential_directory: str) -> bool:
    """Check if a string is considered a directory."""
    regex_dir = r'^dir\s[a-zA-Z/]+$'
    return bool(re.search(regex_dir, potential_directory))


class ParseInput:
    def __init__(self, data_stream: list[str]):
        self.data_stream = data_stream
        self.dirs = self._parse_directories()

    def _parse_directories(self) -> dict[str, Directory]:
        """
        Create a dictionary mapping the directories to empty lists.

        Does not map directories to other directories or files yet.

        :return: A dictionary containing all the directories and empty lists
        """
        directories = {}

        for line in self.data_stream:
            if not is_directory(line):
                continue

            dir_name = re.search(r'[a-zA-Z/]+$', line)[0]
            directories[dir_name] = Directory(dir_name)

        return directories

    def parse_files(self) -> None:
        """Add files to the appropriate directories."""
        current_dir = '/'

        for line in self.data_stream:
            # change directory
            if is_command(line):
                command = line.split(' ')
                if command[1] == 'cd':
                    current_dir = command[2]

            # add files to directory
            elif is_file(line):
                size, filename = line.split(' ')
                self.dirs[current_dir].append(File(filename, size))



# TODO: restructure this to be in the class instead of standalone.
def create_file_structure(data_stream: list[str]) -> dict[str, list]:
    main_dir = '/'
    directories = {main_dir: []}

    # initialize the dictionary with all directories in the input
    for line in data_stream:
        if is_directory(line):
            dir_name: str = line.split()[1]

            directories[dir_name] = []

    current_directory = main_dir
    for line in data_stream:
        if is_command(line):
            cmd = line.split(line)

            if cmd[1] == 'cd':

                # changing current directory
                if cmd[2].isalpha() or cmd[2] == '/':
                    current_directory = cmd[2]

    return directories