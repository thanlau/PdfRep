# Extract Paths from PDF Files

# This script extracts object paths from PDF files using the pdf_genome library.

# How to Use:
# 1. Replace the `folder_path` variable with the path to your PDF files.
# 2. Replace the existing pdf_genome.py file in the pdfrw library path with this script.

import pickle
import os
from pdf_genome import PdfGenome
import types

def is_picklable(obj):
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PicklingError, TypeError):
        return False
      
# Set the folder path to the directory containing your PDF files.      
folder_path = "/home/pluto/ran/data/MALWARE_PDF_PRE_04-2011_10982_files"

res = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        try:
            pdf_obj = PdfGenome.load_genome(file_path, pickleable=True)
            paths = PdfGenome.get_object_paths(pdf_obj)
            if is_picklable(paths):
                result = {
                    "filename": filename,
                    "paths": paths
                }
                res.append(result)
        except:
            continue



with open('maliciousPaths_contagio.pkl', 'wb') as file:
    pickle.dump(res, file)
