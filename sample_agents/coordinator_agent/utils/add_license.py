#!/usr/bin/env python3
"""
Utility script to add the Apache license header to all Python files in the utils folder.
"""

import os
import glob

LICENSE_HEADER = """# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

def add_license_to_file(file_path):
    """Add the license header to a file if it doesn't already have it."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the license is already there
    if content.startswith("# Copyright 2025 Google LLC"):
        print(f"License already exists in {file_path}")
        return False
    
    # Add the license
    with open(file_path, 'w') as f:
        f.write(LICENSE_HEADER + "\n" + content)
    
    print(f"Added license to {file_path}")
    return True

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = glob.glob(os.path.join(script_dir, "*.py"))
    
    # Skip this script itself
    py_files = [f for f in py_files if not f.endswith("add_license.py")]
    
    added_count = 0
    for file_path in py_files:
        if add_license_to_file(file_path):
            added_count += 1
    
    print(f"\nLicense header added to {added_count} files out of {len(py_files)} Python files.")

if __name__ == "__main__":
    main() 