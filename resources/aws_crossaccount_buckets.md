# Sharing AWS bucket access walk-through

Here's a log of what we did to get access to each other's AWS S3 buckets.

## Before you begin

Collect the following information from UserA (the bucket owner) and
UserB (the user accessing the bucket):

- UserA:
  - The bucket resource id, should look like `arn:aws:s3:::bucket-name`

- UserB:
  - Their IAM user ARN, should look like `arn:aws:iam::123456789012:user/IAM-name`
  - Their IAM user Access Key ID, should look like `AKIAIOSFODNN7EXAMPLE`
  - Their IAM user Secret Access Key, should look like `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

## Update bucket permissions
UserA should attach the policy below to the S3 bucket:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": ["arn:aws:iam::123456789012:user/IAM-name",
                        "arn:aws:iam::234567890123:user/IAM-name"]
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::bucket-name/*"
            ]
        }
    ]
}
```

## Attach user policy
Attach the policy below to UserB's IAM user:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::bucket-name/*"

        }
    ]
}
```

## Install AWS CLI
UserB needs to install AWS CLI version 2, this is necessary for storing your
credentials so that you can access the bucket.
Directions can be found at https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

After installing, run `aws config` in the terminal. It will ask you to enter
your Access Key ID and Secret Access Key. For your region enter `us-east-1` (or
your local equivalent). You can leave output blank.

From here, you can use the AWS CLI to push/pull files to the bucket. As an example,
the following code synchronizes the contents of an Amazon S3 folder named path
in my-bucket with the current working directory.
```
$ aws s3 sync . s3://my-bucket/path
upload: MySubdirectory\MyFile3.txt to s3://my-bucket/path/MySubdirectory/MyFile3.txt
upload: MyFile2.txt to s3://my-bucket/path/MyFile2.txt
upload: MyFile1.txt to s3://my-bucket/path/MyFile1.txt
```
Switching the order of `.` and `s3://my-bucket/path` would sync the folder with
the bucket.

## Python & AWS with boto3
Example code:
```
import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucket')
bucket.download_file('/path/to/file/hello.txt', '/path/to/file/hello.txt')
```
