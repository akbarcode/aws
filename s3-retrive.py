import boto3
# import json
s3 = boto3.client('s3')
response = s3.list_buckets()
# print response
Output = []

def add_tag_bucket(bucket_name, kms_value):
    bucket_tagging = s3.get_bucket_tagging(Bucket=bucket_name)
    old_tags = {i['Key']: i['Value'] for i in bucket_tagging['TagSet']}
    old_tags['KMS'] = True
    try:
        response = s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [{'Key': str(k), 'Value': str(v)} for k, v in old_tags.items()]
            }
        )
    except:
        print(f'Could not able to add/append tag to this bucket: {bucket_name}')

for bucket in response['Buckets']:
#    print (bucket["Name"])
    try:
        enc = s3.get_bucket_encryption( Bucket = bucket["Name"])
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        # print (type(rules))
        if 'aws:kms' in str(rules) :
            print ('%s bucket is encrypted with kms' % bucket["Name"])
            add_tag_bucket(bucket["Name"], True)
        else:
            Output.append(bucket["Name"])
        # ['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
    except:
        # print('%s bucket not encrypted' % bucket["Name"])
        Output.append(bucket["Name"])
        add_tag_bucket(bucket["Name"], False)
print ( "list of bucket without default (kms ) encryption are :" )
print(Output) 
