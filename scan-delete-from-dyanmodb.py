from boto3.dynamodb.conditions import Key, Attr
import boto3
import json
import decimal
#from __future__ import print_function # Python 2/3 compatibility
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('table-name')

result_item = []
# Find item that does not contain value
result_data = table.scan(
    FilterExpression= ~Attr('item').contains("value1") & ~Attr('item').contains("value2") ,
)

#print result_data

result_item.extend(result_data['Items'])
print len(result_data['Items'])

while 'LastEvaluatedKey' in result_data:
    result_data = table.scan(
        FilterExpression= ~Attr('item').contains("value1") & ~Attr('item').contains("value2") ,
        ExclusiveStartKey=result_data['LastEvaluatedKey']
    )
    result_item.extend(result_data['Items'])


counter = 0
temp_dict = {}
for each_record in result_item:
    print(each_record)
    counter = counter + 1
    print (counter)
    # to delete
# relplace primary-key and item    
    table.delete_item(Key={'primary-key': dict(each_record)['primary-key'], 'item': dict(each_record)['item']})
    # to insert
#    table.put_item(Item=dict(each_record))
