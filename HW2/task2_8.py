import os

# Path to the folder with HL7 files
folder_path = "Clinical_HL7_Samples/"

# Function to process an HL7 message and find the youngest male patient
def extract_patient_info(hl7_message):
    segments = hl7_message.split('\n')
    birth_year, gender = None, None
    
    for segment in segments:
        # Looking for the PID segment
        if segment.startswith('PID'):
            fields = segment.split('|')
            if len(fields) > 8:
                birth_date = fields[7]
                gender = fields[8]
                
                # Check if birth date is present and gender is male ('M')
                if birth_date and gender == 'M':
                    try:
                        birth_year = int(birth_date[:4])
                    except ValueError:
                        continue
    
    return birth_year, gender

# Loop through all subfolders and files
youngest_birth_year = None

for root, _, files in os.walk(folder_path):
    for file_name in files:
        # Ignore system files, e.g., .DS_Store
        if file_name.startswith('.'):
            continue

        # Construct the full path to the file
        file_path = os.path.join(root, file_name)

        # Try to open the file with different encodings
        hl7_message = None
        for encoding in ['utf-8', 'latin1']:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    hl7_message = file.read()
                    break
            except (UnicodeDecodeError, IOError):
                continue

        # If unable to read the file, skip it
        if hl7_message is None:
            print(f"Failed to read the file {file_path}")
            continue

        # Process the HL7 message
        birth_year, gender = extract_patient_info(hl7_message)
        
        # Update information about the youngest male patient
        if gender == 'M' and birth_year is not None:
            if youngest_birth_year is None or birth_year > youngest_birth_year:
                youngest_birth_year = birth_year

# Output the result
if youngest_birth_year:
    print(f"The youngest male patient was born in {youngest_birth_year}")
else:
    print("No male patients were found.")
