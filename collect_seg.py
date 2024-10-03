import os
import shutil
import nibabel as nib
import sys
import numpy as np

def main(run_mode):
    src_path = os.path.join(os.getcwd(), 'cc359ppmi_first', 'data')
    src_folders = os.listdir(src_path)
    
    # 조건에 맞는 폴더만 리스트에 남깁니다.
    src_folders = [folder for folder in src_folders if os.path.exists(os.path.join(src_path, folder, '1_striatum_first.nii.gz'))]
    src_folders = [folder for folder in src_folders if os.path.exists(os.path.join(src_path, folder, '2_striatum_first.nii.gz'))]
    src_folders = [folder for folder in src_folders if os.path.exists(os.path.join(src_path, folder, '3_striatum_first.nii.gz'))]

    for src_folder in src_folders:
        if run_mode in [1]: print(src_folder)
    print(f'{len(src_folders)} patients are ready')
    for i, src_folder in enumerate(src_folders):
        print(i+1, src_folder)

    
    trg_path = os.path.join(os.getcwd(), 'cc359ppmi_first', 'data2')
    os.makedirs(trg_path, exist_ok=True)
    # 초기화: 최종 라벨 데이터를 저장할 배열
    for src_folder in src_folders:
        sub_list = ['striatum_first.nii.gz', '3_striatum_first.nii.gz', '2_striatum_first.nii.gz', '1_striatum_first.nii.gz']
        label_list = [3,4,2,1]
        dst_folder = os.path.join(trg_path, src_folder)
        # mri_file = os.path.join(src_path, src_folder, 'brain.nii.gz')
        os.makedirs(dst_folder, exist_ok=True)
        final_data = None
        for subregion, label_postfix in zip(sub_list, label_list):
            src_file = os.path.join(src_path, src_folder, subregion)
            # pet_file = os.path.join(src_path, src_folder, 'realigned_pet.nii.gz')
            proxy = nib.load(src_file)
            data = proxy.get_fdata()
            affine = proxy.affine
            active_mask = np.isin(data, [11, 12, 26, 50, 51, 58])
            active_data = np.where(active_mask, data, 0)
            active_data[active_data == 11] = 11 * 10 + label_postfix # L Caudate
            active_data[active_data == 12] = 12 * 10 + label_postfix # L Putamen
            active_data[active_data == 26] = 26 * 10 + 1 # L Accumbens
            active_data[active_data == 50] = 50 * 10 + label_postfix # R Caudate
            active_data[active_data == 51] = 51 * 10 + label_postfix # R Putamen
            active_data[active_data == 58] = 58 * 10 + 1 # R Accumbens
            # 최종 데이터 배열 초기화
            if final_data is None:
                final_data = np.zeros_like(active_data)

            # 0이 아닌 값을 가진 픽셀만 덮어쓰기
            nonzero_mask = active_data != 0
            final_data[nonzero_mask] = active_data[nonzero_mask]
        # 최종 데이터를 NIfTI 이미지로 저장
        # shutil.copy2(mri_file, os.path.join(dst_folder, 'brain.nii.gz'))
        # shutil.copy2(pet_file, os.path.join(dst_folder, 'realigned_pet.nii.gz'))
        final_img = nib.Nifti1Image(final_data, affine)
        nib.save(final_img, os.path.join(dst_folder, 'striatum_first_sub.nii.gz'))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_mode = int(sys.argv[1])
        main(run_mode)
    else:
        main(run_mode=0)