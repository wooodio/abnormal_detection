from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from api.analyzeVideo import analyze_video
from api.dataProcess import split_mp4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['IMAGE_FOLDER'] = os.path.join(app.root_path, 'jpg_url')
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if uploaded_file and allowed_file(uploaded_file.filename):
            # Save the uploaded file to the specified folder
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)
            #streamlit으로부터 전송받은 영상 split
            print('1')
            print(filepath)
            split_mp4(filepath, app.config['IMAGE_FOLDER'])
            #split한 이미지 분석
            analyze_video(app.config['IMAGE_FOLDER'])

            return jsonify({"message": "File uploaded successfully!"}), 200
        else:
            return jsonify({"error": "Invalid file format"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
