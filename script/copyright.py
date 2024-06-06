# MIT License
#
# Copyright (c) 2023-2024 Developers of NodeCloud.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pathlib
import re
from datetime import datetime
import argparse
import shutil

def load_license_header():
    with open('LICENSE', 'r') as file:
        license_header = file.read()
    return license_header

def format_as_comment(license_header, ext):
    if ext == 'python':
        comment_lines = ["# " + line if line.strip() != "" else "#" for line in license_header.split('\n')]
        comment_lines.append("\n")
    elif ext == 'cpp':
        comment_lines = ["// " + line if line.strip() != "" else "//" for line in license_header.split('\n')]
    return '\n'.join(comment_lines)

# Define the current year
initial_year = 2023
current_year = datetime.now().year

# File extensions to search for
extensions = ['.cpp', '.hpp', '.py']

# Directories to search in
directories = ['interface', 'script', 'pynodecloud']

license_header = load_license_header()

license_header_python = format_as_comment(license_header, 'python')

license_header_cpp = format_as_comment(license_header, 'cpp')

def is_license_in_first_lines(file_path, num_lines=5):
    with open(file_path, 'r') as file:
        for _ in range(num_lines):
            line = file.readline()
            if "(c)" in line:
                return True
    return False

# Update license year in C++ and Python files
def update_add_license():
    previous_length = 0
    found_file_counter = 0
    update_file_counter = 0
    for directory in directories:
        for ext in extensions:
            for file in pathlib.Path(directory).rglob(f'*{ext}'):
                print(str(file).ljust(max(len(str(file)), previous_length)), end='\r', flush=True)
                previous_length = len(str(file))
                
                found_file_counter += 1
                
                with open(file, 'r+') as f:
                    if is_license_in_first_lines(file):
                        continue
                    
                    content = f.read()
                    
                    # Add license header if not present
                    if ext == '.py':
                        content = license_header_python + content
                    else:
                        content = license_header_cpp + content
                        
                    # Write updates back to the file
                    f.seek(0)
                    f.write(content)
                    f.truncate()

    print("Found {} files, updated {} files.".format(found_file_counter, update_file_counter))
    print("License years updated to {}.".format(current_year))
    
def remove_license():
    for directory in directories:
        for ext in extensions:
            for file in pathlib.Path(directory).rglob(f'*{ext}'):
                try:
                    with open(file, 'r+') as f:
                        content = f.read()

                        # Remove the license header
                        if ext == '.py':
                            license_pattern = license_header_python
                        else:
                            license_pattern = license_header_cpp
                        content = re.sub(re.escape(license_pattern), '', content, flags=re.MULTILINE)

                        f.seek(0)
                        f.write(content)
                        f.truncate()
                        
                except IOError as e:
                    print(f"Error updating file {file}: {e}")
                    
    print("License removed.")
    
if __name__ == "__main__":
    os.system("clear")
    
    parser = argparse.ArgumentParser(description='copyright')
    
    parser.add_argument('--update', action='store_true', help='update and add license')
    parser.add_argument('--remove', action='store_true', help='remove license')
    
    args, unknown = parser.parse_known_args()
    
    if args.update:    
        update_add_license()
    
    if args.remove:
        remove_license()