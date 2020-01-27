import boto3
# import json
s3 = boto3.client('s3')
response = s3.list_buckets()
# print response
Output = []
for bucket in response['Buckets']:
#    print (bucket["Name"])
    try:
        enc = s3.get_bucket_encryption( Bucket = bucket["Name"])
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        # print (type(rules))
        if 'aws:kms' in str(rules) :
            print ('%s bucket is encrypted with kms' % bucket["Name"])
        else:
            Output.append(bucket["Name"])
        # ['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
    except:
        # print('%s bucket not encrypted' % bucket["Name"])
        Output.append(bucket["Name"])
print ( "list of bucket without default (kms ) encryption are :" )
print(Output) 
