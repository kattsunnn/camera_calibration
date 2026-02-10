import sys
from pathlib import Path
import numpy as np

def get_file_paths(dir_path: str, pattern: str) :
    dir_path = Path(dir_path)
    if not dir_path.exists():
        raise FileNotFoundError()
    file_paths = sorted([str(p) for p in dir_path.glob(pattern)])
    for file_path in file_paths:
        print(file_path)
    return file_paths

extrinsics_dir = sys.argv[1]
r_ppi_dir = sys.argv[2]
output_dir = Path(sys.argv[3]) 

output_dir.mkdir(parents=True, exist_ok=True)

extrinsics_paths = get_file_paths(extrinsics_dir, "*extrinsics*")
r_ppi_paths = get_file_paths(r_ppi_dir, "*ppi_r*")

extrinsics_ref_list = []
for extrinsics_path, r_ppi_path in zip(extrinsics_paths,  r_ppi_paths):
    extrinsics = np.loadtxt(extrinsics_path)
    r_mat = extrinsics[:3, :]
    t_vec = extrinsics[3, :].reshape(3, 1)
    r_ppi = np.loadtxt(r_ppi_path)
    r_ref = r_ppi @ r_mat
    t_ref = r_ppi @ t_vec
    extrinsics_ref = np.vstack([r_ref, t_ref.reshape(1, 3)])
    extrinsics_ref_list.append(extrinsics_ref)

for idx, extrinsics_ref in enumerate(extrinsics_ref_list):
    file_name = f"camera{idx+1:02}_extrinsics_ref"
    np.savetxt(Path(output_dir)/Path(file_name).with_suffix(".dat"), extrinsics_ref)
    