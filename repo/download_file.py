import boto3
import botocore
import os

def run(bucket, file):
    print("the file name is : ")
    print(file)
    print(bucket)
    destination = '/DownloadFolder/'+file
    #print(destination)
    s3 = boto3.resource('s3')
    #s3.meta.client.download_file(bucket, file, destination)
    op_dir = os.path.join('/home/ubuntu/repo/DownloadFolder', file)
    print(op_dir)
    s3.meta.client.download_file(bucket, file, op_dir)


def list_files(bucket, file):
    keys = []
    kwargs = {'Bucket': bucket, 'Prefix': file}
    s3 = boto3.client('s3')
    resp = s3.list_objects(**kwargs)
    for file in resp['Contents']:
        keys.append(file['Key'])
    return len(keys)