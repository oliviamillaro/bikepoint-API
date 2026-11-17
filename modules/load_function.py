import os
import boto3
import logging

logger = logging.getLogger(__name__)

def load_to_s3(AWS_ACCESS_KEY:str, AWS_SECRET_ACCESS_KEY:str, AWS_BUCKET_NAME:str, data_dir:str):
    """_summary_

    Args:
        AWS_ACCESS_KEY (str): Key value (get value from your .env in main)
        AWS_SECRET_ACCESS_KEY (str): Secret value (get value from your .env in main)
        AWS_BUCKET_NAME (str): Bucket name (get value from your .env in main)
        data_dir (str): Filepath where the data was extracted to
    """
    
    file_location = os.listdir(data_dir)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    #first variable of s3_client.upload_file is where the file is locally, second is bucket, third is rename it when it gets to S3
    for file in file_location:
        to_upload = f'{data_dir}/{file}'
        s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file)
        logger.info(f'{file} uploaded to S3')
        os.remove(to_upload)