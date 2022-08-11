import boto3

def detect_text(photo, bucket):


    client=boto3.client('rekognition', region_name='ap-south-1')


    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    return len(textDetections)

def main():
    s3client=boto3.client('s3', region_name='ap-south-1')

    for key in s3client.list_objects(Bucket='mysecondawsbucketsahil')['Contents']:
        print('Printing key' + key['Key'])  
        bucket='mysecondawsbucketsahil'
        photo=key['Key']
        text_count=detect_text(photo,bucket)
        print("Text detected: " + str(text_count))


if __name__ == "__main__":
    main()