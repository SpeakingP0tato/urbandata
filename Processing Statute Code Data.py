import pandas as pd
import re

# 파일 경로 설정
xlsx_file_path = '토지이용계획공간정보_코드_시유외재산목록.xlsx'
code_file_path = '법령 코드 분류.xlsx'

# 1. 엑셀 파일 (토지이용계획공간정보_코드_시유외재산목록.xlsx) 불러오기
df_excel = pd.read_excel(xlsx_file_path, dtype={'PNU': str})

# 2. 법령 코드 분류 엑셀 파일 불러오기
df_code = pd.read_excel(code_file_path, dtype=str)

# 3. 법령 코드 분류에 따른 전체 UNIT 구분 (NaN 값 제외)
df_code_non_null = df_code.dropna(subset=['UNIT'])
all_units = df_code_non_null['UNIT'].unique()

# 4. 모든 데이터를 저장할 딕셔너리 생성 (UNIT 별로 데이터 저장)
unit_data_dict = {unit: [] for unit in all_units}

# "코드_"로 시작하는 모든 컬럼들을 추출합
code_columns = [col for col in df_excel.columns if col.startswith('코드_')]

# 각 "코드_" 컬럼에 대해 법령 코드 분류 데이터와 매칭하여 UNIT 정보를 추가하고 추출
for idx, row in df_excel.iterrows():
    pnu = row['PNU']
    matching_data = {}  # 각 PNU에 대해 UNIT별 매칭 데이터를 임시 저장

    for code_col in code_columns:
        if pd.notna(row[code_col]):
            full_code = row[code_col]  # 결합된 코드 전체
            
            # "_3.0"이 포함된 코드는 건너
            if "_3.0" in full_code:
                continue

            # 코드 값에서 접미사 (_3.0, _2.0, _1.0 등)를 분리
            match = re.match(r"([A-Z0-9]+)(_.*)", full_code)
            if match:
                code_value = match.group(1)
                suffix = match.group(2)
            else:
                code_value = full_code
                suffix = ""

            # 접미사 변환
            if suffix == "_1.0":
                suffix = ""  # _1.0은 표기하지 않음
            elif suffix == "_2.0":
                suffix = "(저촉)"  # _2.0은 (저촉)으로

            # 법령 코드 분류 데이터에서 UCODE에 매칭되는 모든 경우 확인
            matched_units = df_code[df_code['UCODE'] == code_value]
            for _, matched_row in matched_units.iterrows():
                unit = matched_row['UNIT']
                unit_name = matched_row['UNAME']  # 법령 코드의 한글 이름 가져오기
                # 한글 이름 뒤에 접미사를 붙여 변환
                translated_code = f"{unit_name}{suffix}"

                if unit not in matching_data:
                    matching_data[unit] = {'PNU': pnu, '코드': []}

                # 같은 UNIT에 대해 여러 코드가 있으면 모두 추가
                matching_data[unit]['코드'].append(translated_code)

    # 매칭된 데이터를 UNIT별로 저장
    for unit, data in matching_data.items():
        unit_data_dict[unit].append(data)

# UNIT별로 파일을 생성하여 저장
for unit, rows in unit_data_dict.items():
    # 각 UNIT에 해당하는 데이터프레임 생성
    unit_rows = []
    for row in rows:
        unit_row = {'PNU': row['PNU']}
        # 코드들을 개별 열로 추가
        for idx, code in enumerate(row['코드']):
            unit_row[f'코드_{idx + 1}'] = code
        unit_rows.append(unit_row)

    df_unit = pd.DataFrame(unit_rows)

    # 파일 이름에 UNIT명을 포함하여 저장
    if not df_unit.empty:
        unit_name = unit.replace(" ", "_").replace("/", "_")
        output_file_path = f'(셀분리)(시유외)PNU별_법령_구분_결과({unit_name})_코드한글변환.xlsx'
        df_unit.to_excel(output_file_path, index=False)
        print(f"{unit} UNIT에 해당하는 파일이 저장되었습니다: {output_file_path}")
    else:
        print(f"{unit} UNIT에 해당하는 데이터가 없어 파일을 저장하지 않았습니다.")
