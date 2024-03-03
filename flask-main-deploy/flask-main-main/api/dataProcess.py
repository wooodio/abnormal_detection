import os
import cv2
from google.cloud import storage 

#1초당 1프레임 추출하고 영상 삭제
def split_mp4(mp4_path,jpg_path):
    vidcap = cv2.VideoCapture(mp4_path)
    
    fps = vidcap.get(cv2.CAP_PROP_FPS)  # 비디오의 프레임 속도를 가져옴
    
    frame_rate = int(fps)  # 비디오의 프레임 속도를 정수로 변환

    success, image = vidcap.read()
    
    count = 0
    frame_number = 0

    while success:
        if frame_number % frame_rate == 0:  # 1초당 1프레임 추출
            cv2.imwrite(f"{jpg_path}/frame_{count}.jpg" , image)  # 프레임을 JPEG 파일로 저장
            count += 1
        success, image = vidcap.read()
        frame_number += 1

    
    #remove_file(mp4_path)
    print("이미지 변환 완료!")
    

#버킷 스토리지에 데이터 저장
def sendStorage(source_file_name, destination_blob_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './json_key/storage_key.json' 
    bucket_name = 'img-for-kakao'
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

#이미지 삭제
def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"파일 '{file_path}'를 삭제하는 동안 오류가 발생했습니다:", e)


