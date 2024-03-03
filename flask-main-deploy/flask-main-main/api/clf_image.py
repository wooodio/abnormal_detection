import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import os

#이미지 분류
def clf_frame(
    project='team03-project',
    endpoint_id="2361392535672193024",
    filename = None,
    location = "us-central1",
    api_endpoint= "us-central1-aiplatform.googleapis.com",
):
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./json_key/vertex_key.json"
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5, max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    
    predictions = response.predictions
    for prediction in predictions:
        display_names = prediction.get("displayNames")[0]
        #display_names = prediction.get("displayNames", [])[0]
        # print(display_names, type(display_names))
        #confidences1 = prediction.get("confidences")[0]
        # print(confidences1, type(confidences1))
        #confidences2 = prediction.get('confidences', [])[1]
        #bbox = prediction.get('bboxes')[0]
        
        return display_names
       