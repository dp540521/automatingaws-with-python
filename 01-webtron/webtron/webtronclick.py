import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
@click.group() ## This is the grouping of different functions under click
def cli():
    "Webtron deploys websites to AWS"       ## Doc String
    pass                                   ## Passes the controls to below child funtions

@cli.command('list-buckets')     ##Decorator that wraps the function
def list_buckets():              ## Function that defines the logic
    "List All S3 Buckets" ## Doc String
    for bucket in s3.buckets.all():
        print (bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "This lists the contents of Bucket"
    for obj in S3.Bucket(bucket).objects.all():
        print(obj)

if __name__ == '__main__':
    cli()
