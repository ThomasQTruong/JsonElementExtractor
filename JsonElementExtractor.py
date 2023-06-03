"""
 * JsonElementExtractor.py
 * Extracts certain data from .json into a new .json file.
 * Can also insert custom elements.
 * 
 * Copyright (c) 2023, Thomas Truong
"""

import os, json


# Input/output file locations.
INPUT_DIR = "./input/"
OUTPUT_DIR = "./output/"

# Output JSON settings.
ELEMENTS_TO_GET = ["forms//aspects", "moves"]
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
      sorted_Subdirectory = sorted(os.listdir(f"{INPUT_DIR}/{file_path}/"))
      
      # For every file in the sub directory.
      for file in sorted_Subdirectory:
        extracted_data = extract_from_json(f"{INPUT_DIR}/{file_path}/{file}")

        # User wants to insert custom elements.
        if INSERT_CUSTOM_ELEMENTS:
          extracted_data = insert_custom_elements(extracted_data, file)
        
        write_output_json(f"{OUTPUT_DIR}/{file_path}/{file}", extracted_data)


"""Extracts data from a json file.

Extracts ELEMENTS_TO_GET from json_path into a dictionary.

Args:
  json_path: The path to the json file.

Returns:
  A dict of the extracted data.
"""
def extract_from_json(json_path) -> dict:
  extracted_data = {}

  # Open and laod data.
  opened_file = open(json_path, "r")
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
        # Special case: no named dictionary inside json.
        if "" in element_location:
            if element_location[2] in file_data[element_location[0]][0].keys():
              extracted_data[element_location[0]] = [{element_location[2]:
                  file_data[element_location[0]][0][element_location[2]]}]
        # Just a regular subdirectory.
        else:
          if element_location[1] in file_data[element_location[0]]:
            extracted_data[element_location[0]] = {element_location[1]:
                file_data[element_location[0]][element_location[1]]}
  
  return extracted_data


"""Calls custom insert functions to insert custom elements.

Args:
  data: the data to insert to.
  file_name: the name of the current file that data is being extracted from.
"""
def insert_custom_elements(data, file_name):
  data = insert_target_element(data, file_name)
  return data


"""Creates and inserts a target element into the dict.

Creates a target key and pairs it with "cobblemon:{file_name}".

Args:
  data: the original data dictionary.
  file_name: the name of the json file.

Returns:
  A dict of the inserted target at the front of the data.
"""
def insert_target_element(data, file_name) -> dict:
  new_data = {"target": f"cobblemon:{file_name.split('.json')[0]}"}
  # Combine both dicts and puts new_data before data.
  new_data.update(data)
  return new_data


"""Writes extracted data into a json file.

Args:
  json_path: The path to the new json file.
  extracted_data: The data that was extracted to write.
"""
def write_output_json(json_path, extracted_data):
  # Directory in path does not exist, create directory.
  if not os.path.exists(os.path.dirname(json_path)):
    os.makedirs(os.path.dirname(json_path))

  # Open/create json file.
  with open(json_path, "w") as output_file:
    json.dump(extracted_data, output_file, indent = INDENTS)


if __name__ == "__main__":
  main()
