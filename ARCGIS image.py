import arcpy
import os

# ArcGIS 프로젝트(.aprx) 파일 경로 지정
project_path = "A-2 획지현황도(일반지도).aprx"
aprx = arcpy.mp.ArcGISProject(project_path)

# 레이아웃 가져오기
layout = aprx.listLayouts("A-2 획지현황도(일반지도)")[0]
map_frame = layout.listElements("MAPFRAME_ELEMENT")[0]  # 맵 프레임 가져오기
map_obj = map_frame.map

# 기존 이미지 파일들이 저장된 폴더 경로
image_folder = "01 항공지도\01 서초구"

# 새로 저장할 이미지 파일 경로
output_folder = "02 일반지도\01 서초구"

# GIS 레이어 이름 및 대표주소 컬럼명
layer_name = "획지"
address_column = "대표주소"

# 폴더 내 파일 이름 리스트
image_files = os.listdir(image_folder)

print(f"Found {len(image_files)} files in the directory.")

# 주소와 축척을 추출
address_scale_pairs = []
for f in image_files:
    if f.lower() == "thumbs.db" or not f.endswith('.jpg'):
        continue

    try:
        base_name = os.path.splitext(f)[0]
        if '(' in base_name and ')' in base_name:
            parts = base_name.split('(')
            if len(parts) == 2 and ')' in parts[1]:
                address = parts[0].strip()
                scale = parts[1].replace(')', '').strip()
                address_scale_pairs.append((address, scale))
    except Exception as e:
        continue

print(f"Total valid address/scale pairs: {len(address_scale_pairs)}")

# 주소별로 일치하는 파일 처리
for pair in address_scale_pairs:
    address, scale = pair

    try:
        # 피처 선택
        arcpy.management.SelectLayerByAttribute(map_obj.listLayers(layer_name)[0], "NEW_SELECTION", f"{address_column} = '{address}'")
        
        # 피처의 중심점으로 시점 이동 및 스케일 설정
        with arcpy.da.SearchCursor(map_obj.listLayers(layer_name)[0], ["SHAPE@"], f"{address_column} = '{address}'") as cursor:
            for row in cursor:
                extent = row[0].extent
                map_frame.camera.setExtent(extent)
                map_frame.camera.scale = float(scale)
                
        # 이미지 내보내기 경로 설정
        output_image_path = os.path.join(output_folder, f"{address}({scale}).jpg")
        
        # 레이아웃을 사용하여 이미지 내보내기
        layout.exportToJPEG(output_image_path, resolution=300)
        print(f"Successfully exported image for {address} with scale {scale}")
        
        # 선택 해제
        arcpy.management.SelectLayerByAttribute(map_obj.listLayers(layer_name)[0], "CLEAR_SELECTION")

    except Exception as e:
        print(f"Failed to export JPEG for {address} with scale {scale}: {e}")
        continue
