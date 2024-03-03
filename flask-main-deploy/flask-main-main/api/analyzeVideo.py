import os
from google.cloud import pubsub_v1
from api.clf_image import clf_frame
from api.dataProcess import remove_file, sendStorage
import time
from datetime import datetime


'''
비디오 분석:
비디오를 1초마다 분류. 이상행동감지시 버킷에 해당 이미지 저장, 
pub-sub에 버킷에 저장된 이미지url, 이상행동, 경과시간 전송
'''
def analyze_video(data_urls):
    
    frame_list = []
    for file_name in os.listdir(data_urls):
        if os.path.isfile(os.path.join(data_urls, file_name)):
            file_path = os.path.join(data_urls, file_name)
            frame_list.append(file_path)

    valid_count = 0
    before_status = 0
    
    for idx, frame in enumerate(frame_list):
        status = clf_frame(filename=frame)
        print(status)

        if status == '정상':
            before_status = 0
            valid_count = 0
            
        elif status in ['폭행', '쓰러짐', '화재']:
            if before_status == 1:
                valid_count += 1

            #5초이상 이상행동 감지시..
            if valid_count == 3:
                print(f'{idx}초에 {status} 발생!')
                current_time = time.time()
                human_readable_time = datetime.now()
                #스토리지 버킷에 저장
                sendStorage(frame,f'test_{int(current_time)}')
                print('스토리지에 저장되었습니다')
                #time이랑, frame으로 얻는 이미지 pub/sub으로
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./json_key/pubsub_key.json"
                
                publisher = pubsub_v1.PublisherClient()
                
                topic_path = 'projects/team03-project/topics/test'
                #storage_url = f'https://storage.cloud.google.com/img-for-kakao/test_{time}'.encode('utf-8')
                storage_url = f'gs://img-for-kakao/test_{int(current_time)}'.encode('utf-8')
                attributes = {
                    'abnormal' : status,
                    'time' : f'{human_readable_time.strftime("%m-%d %H:%M:%S")}'
                }
                publisher.publish(topic_path, storage_url, **attributes)
                print('pub/sub에 전송되었습니다')
                
                
                
            before_status = 1

        print(f'{idx}초 경과, {valid_count}')
        remove_file(frame)  #이미지 삭제

