import pandas as pd
import os
import sys
import subprocess
import re
#read the table


excel_file=sys.argv[1]
output_dir=sys.argv[2]

GEO_sample_tab = pd.read_excel(sys.argv[1], header = None)

print(GEO_sample_tab)

for index, row  in GEO_sample_tab.iloc[2:].iterrows():
    
    code=row[0].strip()
    name=row[1].strip()

    #check if file exists
    if (os.path.exists(output_dir+"/"+name+"_1.fastq.gz")):
        print("File "+name+" already downloaded! \n")
        continue

    print("prefetch.2.11.2 -v "+code)

    message = subprocess.run(["prefetch.2.11.2", "-v", code], capture_output=True)
    nice_message = message.stderr.decode('utf-8')

    regex = re.compile("\w*SRR\w*")
    matched_code = regex.findall(nice_message)[5]
    print("\nConverted SRA id --> " + matched_code)
    #now get fastq files
    subprocess.run(["fastq-dump.2.11.2","--gzip","--outdir", output_dir, "--split-files", "/shares/CIBIO-Storage/GROUPS/sharedLC/Davide/ncbi-geo/sra/"+ matched_code + ".sra" ])

    #change name 
    subprocess.run(["mv", output_dir+"/"+matched_code+"_1.fastq.gz", output_dir+"/"+name+"_1.fastq.gz"])
    subprocess.run(["mv", output_dir+"/"+matched_code+"_2.fastq.gz", output_dir+"/"+name+"_2.fastq.gz"])

