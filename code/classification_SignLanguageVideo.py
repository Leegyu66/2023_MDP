import os

# 수어 데이터 file name에 "_F"가 있으면 정면을 보고 촬영한 영상이다
file_list = ["02", "02-1", "03", "03-1", "04", "04-1", "05", "05-1", "06", "06-1", "07", "07-1", ]
file_path = os.path.join("D:")
file_dir = []
files = os.listdir(file_path)
files_dir = [i for i in files if "_real" in i]
for i, j in enumerate(files_dir):
    file_dir.append(os.path.join(j, file_list[i]))

# 파일 목록을 순회하면서 특정 문자열을 포함하지 않은 파일 삭제
for i in range(len(file_dir)):
    files = os.listdir(os.path.join(file_path, file_dir[i]))
    for file in files:
        file = os.path.join(file_path, file_dir[i], file)
        if "_F" in file:
            print(f"{file} 유지함 (포함하는 문자열 있음)")
        else:
            os.remove(file)
            print(f"{file} 삭제됨")
