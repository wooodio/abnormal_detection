import os
from google.cloud import storage


def parse_url(url):
    bucket_name, img_name = url.split('/')[2:4]

    return (bucket_name, img_name)


def download_image(url):
    KEY_PATH = './gcp.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_PATH

    bucket_name, img_name = parse_url(url)

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(img_name)

    local_filename = f'./static/ab_img/{img_name}'

    blob.download_to_filename(local_filename)

    return local_filename


print(parse_url('gs://img-for-kakao/test_1708494152')[1])
