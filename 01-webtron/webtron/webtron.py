import boto3
import click
from botocore.exceptions import ClientError

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
    "This is to display the contents of Bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Setup and Configure Bucket"
    s3_bucket = None
    s3_bucket = s3.create_bucket(
    Bucket=bucket,
    CreateBucketConfiguration={'LocationConstraint':session.region_name})

    try:
        s3_bucket = s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint':session.region_name}
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
           s3_bucket = s3.Bucket(bucket)
        else:
           raise e

    policy ="""
    {
      "Version":"2012-10-17",
      "Statement":[{
        "Sid":"PublicReadGetObject",
      "Effect":"Allow",
      "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
          ]
        }
      ]
    }
    """% s3_bucket.name
    policy = policy.strip()

    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
    'ErrorDocument': {
                'Key': 'error.html'
                 },
    'IndexDocument': {
                'Suffix': 'index.html'
                 }
        })
    return

if __name__ == '__main__':
    cli()
