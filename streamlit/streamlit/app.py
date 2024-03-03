import streamlit as st
import requests

def page1():
    st.title('CCTV 영상처리')
    st.subheader('이상행동 감지하고 싶은 동영상 업로드')

    # Upload video file
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mkv"])

    if uploaded_file is not None:
        # Display a smaller preview of the uploaded video
        st.video(uploaded_file, format='video/mp4', start_time=0)

        # Button to trigger video upload to the server
        if st.button("Send Video to Server"):
            try:
                # Send the video file to the Flask server
                flask_server_url = "https://abnormal-api.n-e.kr/upload"
                files = {'file': ('uploaded_video.mp4', uploaded_file.read(), 'video/mp4')}
                response = requests.post(flask_server_url, files=files)

                if response.status_code == 200:
                    st.success("File uploaded successfully!")
                    st.json(response.json())  # Display the server's response for testing purposes
                else:
                    st.error(f"Error uploading file. Please try again.{(response.status_code)}")
            except Exception as e:
                st.write(e)
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    page1()
