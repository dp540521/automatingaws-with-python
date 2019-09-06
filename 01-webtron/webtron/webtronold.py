import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.command('list-buckets') ##Decorator that wraps the function
def list_buckets(): ## Function that defines the logic
    "List All S3 Buckets" ## Doc String
    for bucket in s3.buckets.all():
        print (bucket)

if __name__ == '__main__':
     list_buckets()
