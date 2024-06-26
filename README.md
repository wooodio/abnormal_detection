# 무인편의점 내 이상행동 감지 프로젝트
## 프로젝트 개요
![image](https://github.com/wooodio/abnormal_detection/assets/127821186/58bc4dcc-f5df-4492-9778-2530bdb0de56)

본 프로젝트는 무인편의점 내에서 발생하는 이상행동을 감지하기 위한 시스템을 개발하는 것을 목표로 합니다.  실시간으로 영상을 분석하고, 이상행동이 감지될 경우 경고알림 발송합니다. 

## 시스템 아키텍처

![image](https://github.com/wooodio/abnormal_detection/assets/127821186/b50353df-953e-4a77-ae01-71688f35fe45)


## 맡은역활

- **이상행동 감지 모델**: GCP내 Auto ML을 사용하여, 모델을 학습하였습니다.
- **Flask 서버**: streamlit으로 들어오는 이미지를 Auto ML모델에게 보내, 이상행동 유무를 판별합니다.이상행동으로 확인되면, Cloud Storage와 Pub/sub으로 전송합니다.
  (이상행동이 발생한 장면, 발생시각을 Cloud Storage에 저장하고, 자동으로 메신저알림을 위해 Pub/Sub으로 전송합니다.)

### 문제 상황
Google Cloud Platform (GCP)에서 동영상용 모델 배포가 불가능하다는 문제가 발생했습니다. 학습은 가능했지만 배포는 불가능했습니다.

### 해결 방법
동영상을 프레임단위 이미지로 분할하여, 개별 이미지를 분류하는 모델을 개발했습니다. 이를 통해 어느 시점에 이상행동이 발생하였는지 파악할 수 있게 되었습니다. 

## 시연
![스크린샷 2024-04-11 230313](https://github.com/wooodio/abnormal_detection/assets/127821186/8635f300-663c-4176-a851-8ef9c229bf5b)
