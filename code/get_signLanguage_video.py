import json
import os
import pandas as pd


# 1. JSON 파일에서 데이터 로드하기 배열로
folder_paths = [
    r'C:\Users\User\Downloads\수어 영상\2.Validation\01_real_word_morpheme\morpheme\17',
    r'C:\Users\User\Downloads\수어 영상\2.Validation\01_real_word_morpheme\morpheme\18'
]

output_folder = r'D:\수어 번역'

for folder_path in folder_paths:
    names = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('data', []):
                    name = item.get('attributes', [{}])[0].get('name', '')
                    if name:
                        names.append(name)

    # DataFrame으로 변환해주기
    df = pd.DataFrame(names, columns=['Name'])

    # 파일 이름 만들기
    validation_name = folder_path.split('\\')[-3].split('2.Validation')[-1]
    last_number = folder_path.split('\\')[-1]
    excel_file_name = f"{validation_name}_{last_number}.xlsx"

    # 엑셀 파일 저장
    df.to_excel(f"D:\\handword\\{excel_file_name}", index=False)
    #종료 확인용 출력
    print("저장 했습니다." + excel_file_name)