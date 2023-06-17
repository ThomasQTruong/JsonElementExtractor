"""
 * JsonElementExtractor.py
 * Extracts certain data from .json into a new .json file.
 * Can also insert custom elements.
 * 
 * Copyright (c) 2023, Thomas Truong
"""

import os
import json


# Input/output file locations.
INPUT_DIR = "./input/"
OUTPUT_DIR = "./output/"

# Output JSON settings.
"""
Meanings:
/ - indicates regular case (no list).
// - indicates special case (inside a list).

Examples:
moves
  - "moves": ...
baseStats/hp
  - "baseStats": {}
    - Regular case, no list.
forms//aspects
  - "forms": [{"aspects": ...}]
    - Special case, inside a list.
"""
ELEMENTS_TO_GET = ["forms//aspects", "forms//moves", "moves"]
INDENTS = 4
INSERT_CUSTOM_ELEMENTS = True


def main():
  # Gets and sorts directory.
  sorted_directory = sorted(os.listdir(INPUT_DIR))

  # For every file or folder in the input directory.
  for file_or_folder in sorted_directory:
    file_path = f"{file_or_folder}"
    # Is a JSON file.
    if os.path.isfile(file_or_folder):
      extracted_data = extract_from_json(f"{INPUT_DIR}/{file_path}")

      # User wants to insert custom elements.
      if INSERT_CUSTOM_ELEMENTS:
        extracted_data = insert_custom_elements(extracted_data, file_or_folder)

      write_output_json(f"{OUTPUT_DIR}/{file_path}", extracted_data)
    # Is a folder, get JSON files in folders.
    else:
      # Get files in subdirectory.
      sorted_subdirectory = sorted(os.listdir(f"{INPUT_DIR}/{file_path}/"))

      # For every file in the sub directory.
      for file in sorted_subdirectory:
        extracted_data = extract_from_json(f"{INPUT_DIR}/{file_path}/{file}")

        # User wants to insert custom elements.
        if INSERT_CUSTOM_ELEMENTS:
          extracted_data = insert_custom_elements(extracted_data, file)

        write_output_json(f"{OUTPUT_DIR}/{file_path}/{file}", extracted_data)


def extract_from_json(json_path) -> dict:
  """Extracts data from a json file.

  Extracts ELEMENTS_TO_GET from json_path into a dictionary.

  Args:
    json_path: The path to the json file.

  Returns:
    A dict of the extracted data.
  """
  extracted_data = {}

  # Open and laod data.
  with open(json_path, "r", encoding = "utf-8") as opened_file:
    file_data = json.load(opened_file)

    # For every element to extract.
    for element in ELEMENTS_TO_GET:
      element_location = element.split("/")
      # Is main element.
      if len(element_location) == 1:
        # Element exists.
        if element_location[0] in file_data:
          extracted_data[element] = file_data[element]
      # Is a sub-element.
      else:
        # Parent element exists.
        if element_location[0] in file_data:
          # Special case: list of dictonary.
          if "" in element_location:
            # Sub-element exists in json file.
            if element_location[2] in file_data[element_location[0]][0].keys():
              # No dictionary yet, create list of empty dictionary.
              if element_location[0] not in extracted_data:
                extracted_data[element_location[0]] = [{}]

              extracted_data[element_location[0]][0].update({element_location[2]
                      : file_data[element_location[0]][0][element_location[2]]})
          # Regular case: just a dictionary.
          else:
            # Sub-element exists.
            if element_location[1] in file_data[element_location[0]]:
              # No dictionary yet, create empty dictionary.
              if element_location[0] not in extracted_data:
                extracted_data[element_location[0]] = {}
              extracted_data[element_location[0]].update({element_location[1]
                      : file_data[element_location[0]][element_location[1]]})

  return extracted_data


def insert_custom_elements(data, file_name):
  """Calls custom insert functions to insert custom elements.

  Args:
    data: the data to insert to.
    file_name: the name of the current file that data is being extracted from.
  """
  data = insert_target_element(data, file_name)
  return data


def insert_target_element(data, file_name) -> dict:
  """Creates and inserts a target element into the dict.

  Creates a target key and pairs it with "cobblemon:{file_name}".

  Args:
    data: the original data dictionary.
    file_name: the name of the json file.

  Returns:
    A dict of the inserted target at the front of the data.
  """
  new_data = {"target": f"cobblemon:{file_name.split('.json')[0]}"}
  # Combine both dicts and puts new_data before data.
  new_data.update(data)
  return new_data


def write_output_json(json_path, extracted_data):
  """Writes extracted data into a json file.

  Args:
    json_path: The path to the new json file.
    extracted_data: The data that was extracted to write.
  """
  # Directory in path does not exist, create directory.
  if not os.path.exists(os.path.dirname(json_path)):
    os.makedirs(os.path.dirname(json_path))

  # Open/create json file.
  with open(json_path, "w", encoding = "utf-8") as output_file:
    json.dump(extracted_data, output_file, indent = INDENTS)


if __name__ == "__main__":
  main()
