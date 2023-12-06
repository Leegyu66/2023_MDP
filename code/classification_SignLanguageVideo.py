import os
import json
import pandas as pd

# # 수어 데이터 file name에 "_F"가 있으면 정면을 보고 촬영한 영상이다
# file_list = ["10", "10-1", "11", "11-1", "12", "12-1", "13", "13-1", "14", "14-1", "15", "15-1", "16", "16-1"]
# file_path = os.path.join("D:")
# file_dir = []
# files = os.listdir(file_path)
# files_dir = [i for i in files if "_real" in i]
# files_dir = files_dir[16:]

# for i, j in enumerate(files_dir):
#     file_dir.append(os.path.join(j, file_list[i]))

# # 파일 목록을 순회하면서 특정 문자열을 포함하지 않은 파일 삭제
# for i in range(len(file_dir)):
#     files = os.listdir(os.path.join(file_path, file_dir[i]))
#     for file in files:
#         file = os.path.join(file_path, file_dir[i], file)
#         if "_F" in file:
#             print(f"{file} 유지함 (포함하는 문자열 있음)")
#         else:
#             os.remove(file)
#             print(f"{file} 삭제됨")

folder_path = os.path.join('C:', '/수어데이터', '수어 영상', '1.Training', 'morpheme')
folder_list = os.listdir(folder_path)

for folder in [folder_list[0]]:
    names = []
    file_num = []

    file_path = os.path.join(folder_path, folder)
    file_list = os.listdir(file_path)
    for file in file_list:
        if "_F" in file:
            file_name = file[11:15]
            with open(os.path.join(file_path, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('data', []):
                    name = item.get('attributes', [{}])[0].get('name', '')
                    if "많" in name:
                        file_num.append(file_name)
                        names.append(name)
    print(file_num, names)
    # df = pd.DataFrame({'file_num':file_num, 'names':names})

    # df.to_excel('check_data_all.xlsx', index=False)
     