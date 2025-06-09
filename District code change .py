import pandas as pd
from openpyxl import Workbook

# 파일 경로 설정
file_1 = '토지이용계획공간정보_서울시_V월드_20240712기준.xlsx'
file_2 = '용도지역지구구분코드 조회자료_행정표준코드관리시스템.xls'

# 첫 번째 엑셀 파일 읽기
df1 = pd.read_excel(file_1, dtype={'PNU': str})  # PNU 열을 문자열 형식으로 읽기

# 두 번째 엑셀 파일 읽기
df2 = pd.read_excel(file_2)

# 두 번째 엑셀 파일에서 코드와 한글명 매핑
code_to_name = dict(zip(df2['코드값'], df2['코드값의미']))

# 첫 번째 엑셀 파일의 '용도지역지구코드목록' 컬럼의 각 코드를 한글명으로 변환
def convert_codes(codes):
    if pd.isna(codes):
        return ""
    code_list = codes.split(',')
    return ','.join([code_to_name.get(code, code) for code in code_list])

df1['용도지역지구코드목록'] = df1['용도지역지구코드목록'].apply(convert_codes)

# PNU 열을 문자열 형식으로 유지
df1['PNU'] = df1['PNU'].astype(str)

# 결과를 새로운 엑셀 파일로 저장
output_file = '토지이용계획공간정보.xlsx'

# 새로운 엑셀 파일에 데이터프레임을 쓰기
wb = Workbook()
ws = wb.active

# 컬럼 헤더 추가
ws.append(df1.columns.tolist())

# 데이터 추가
for row in df1.itertuples(index=False, name=None):
    ws.append(row)

# PNU 열을 텍스트 형식으로 설정
for cell in ws['P']:
    cell.value = str(cell.value)
    cell.number_format = '@'

wb.save(output_file)

print(f"변환된 파일이 '{output_file}' 이름으로 저장되었습니다.")
