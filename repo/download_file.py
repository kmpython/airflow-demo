import boto3

def run(bucket, file):
    destination = '/home/ubuntu/DownloadFolder/'+file
    s3 = boto.resource('s3')
    s3.meta.client.download_file(bucket, file, destination)