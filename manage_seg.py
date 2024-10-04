import os
import shutil
import nibabel as nib
import sys
import numpy as np
import glob
import pandas as pd

def main(run_mode=0):
    cases_split = os.path.join("CC359PPMI.csv")
    df = pd.read_csv(cases_split)
    M1 = list(df[df['Measurement_ID']==1]['Subject_ID'])
    M2 = list(df[df['Measurement_ID']==2]['Subject_ID'])
    # print(temp2)

    base_dir = os.getcwd()
    folder_list = glob.glob(os.path.join(base_dir, 'inst_[0-9]*', 'cc*'))\
     + glob.glob(os.path.join(base_dir, 'inst_[0-9]*', 'VMAT*'))
     
    for el in folder_list:
        subj = os.path.basename(el)
        if subj in M1:
            src_file = os.path.join(el, 'striatum_first.nii.gz')
            shutil.copy2(src_file, os.path.join(el, 'striatum_orig.nii.gz'))
        else:
            src_file = os.path.join(el, 'striatum_only.nii.gz')
            shutil.copy2(src_file, os.path.join(el, 'striatum_orig.nii.gz'))

if __name__ == '__main__':
    main()