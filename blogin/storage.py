import boto3

class AwsStorage:
    
    def __init__(self):
        # You can also initialize any client or resource here, if needed for the class
        self.s3 = boto3.client('s3')
    
    def upload_to_s3(self, file_path, bucket, s3_path):
        try:
            self.s3.upload_file(file_path, bucket, s3_path)
            print("S3 finished uploading file", file_path, "to", s3_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        return True