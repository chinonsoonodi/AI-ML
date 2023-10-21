## Lambda Function for Imgae Serialization

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key']   ## TODO: fill in
    bucket = "sagemaker-us-east-1-974339051049"    ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, '/tmp/image.png')
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

## Image Serialization Test Event

{
  "s3_key": "test/bicycle_s_000030.png"
}




## Lambda Function for Image Classification using boto3

import json
import boto3
import base64

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-10-21-12-14-12-998"    ## TODO: fill in

#session= session.Session()
runtime = boto3.Session().client('sagemaker-runtime')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])
    
    #envoke the endpoint using boto3 runtime
    response = runtime.invoke_endpoint(EndpointName = ENDPOINT, ContentType = 'image/png',Body = image)
    predictions = json.loads(response['Body'].read().decode())
    
    # We return the data back to the Step Function #Create a new key to the event named   "inferences"  
    event['body']["inferences"] = predictions
    #print(json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': event

        }

## Test Event

{
  "statusCode": 200,
  "body": {
    "image_data": "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",
    "s3_bucket": "sagemaker-us-east-1-974339051049",
    "s3_key": "test/bicycle_s_000030.png",
    "inferences": []
  }
}



## Lambda Fuction for Inference Filtering

import json


THRESHOLD = .70


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['body']['body']['inferences']      ## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any(inference >= THRESHOLD for inference in inferences)     ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

## Test Event

{
  "statusCode": 200,
  "body": {
    "statusCode": 200,
    "body": {
      "image_data": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAPYQAAD2EBqD+naQAAB9dJREFUWIXNl0mTXEcRx3+ZVe/1Oj37PhpZMpblCCRADoMD4+DEgQjgc/Ax/CXgwIkLFw7czAWzhDFrYOMIZAnJCmsZaUaz9PQ23a/fUpUceowMhG8Yky8qKiIPlZn/f1W+/IuZGZ+jKYCZwf8yDTuPCfhnvlkS8tnE+1STz5sC/+Ev3iZWATVBRVBVEBARQBAxRA1BZj5VjPivpxgIAhjPyglEjGgJFgNQYEGxqGCGmaHOIT+89k0ThESURBypOpxzqCpOHc4rzinOOUQUVcX+jScREIMQIhYjJuBDoIrGQB15rJAqQ8pIVUVCCLMVAz5MBzhx4ByoBxRxDtHzPSao9zjzqCpiihN9VroBAtEMQpi5BFwVyULFkyojKCyLUAslGipCVWFVhYaAj+fQmihBhMIJwSlOFXWK90pUT3QOp+fIODereIY60SJRgCTFMEIITKxgOD/Hg0lFv9vlBRK2ZYYuZjPCRPD1SlEVUhMSp3gczhR1DofiTXF1T0xTpiFAhAMtaOHYrFIcRqVKiFD6SD0IVeU46dQ5nXNsxJIlGbOmCXOmkFdU0REqiBE0OCMoVGoEtRmZaqgaohAkUM0lLL3+JW6tKW/GAz4o+vRDSZUoeEEcoBGlpFGVSIyUi00Osj6tszFXG23aGKKCndP18acfXyKYNQczO38JggE1U5rDguzWQ9JhTqfW4OXmBs/rHAGjJCIxkErFQgW1AFjB0mTKjbllGhjTfEoaFY3PeoKdB/XRDD3PiE9kIyIoQu6hIsDeU3aaKVdfvEL6dEh52CNNPShUYmCRSVDOGgnNWspWgLP+mOMyQ7wipWBVeNaUbPZkfYyBKHJ+oyIiRoiBwAyJJAoewwTKRFj7+nWa0dN/+33swT42zRinIJ15mi+8wPLuJo3Hx6Tv3SSWGfOLbbJpRAYRDRGIxPhs+dJFFMMHAUnoOmXUipT1Bt4CnUnOUnQsSGBtLNAb07l+HfeqMn5hm4M//g25uMPmd77F0nKb6Vu/Z+9PfyEed0lcTr2jPKFG4aHuAhYjKgEfAxUR76sITjhNjWFTcZd2aa7UUdrUvCOzEe8dH7LUH3NtrGRv/pneUPnNO7/i+e+9xrU3vs9Zp015+xEPfvAz8g/uUISKXl2ZpNCqJYwXFwkLTR7mZ4SPumzslyyZECzg09Jx5ozjxZTVL2zTDiP0/iOa0wXSWpOyo8yvbnMvOeKdOODlutHZbHHlGzdwR31kOMbf3+f+j39C4+EhznkeNjz97RUubi2y8WjEdJBhk0PSVkJ68SK9do/e/T0u9QwfTOjWoH1pl9okY7F+SvtCSu/RGItQe1qgw0jn4jKDr26RbFxkEqYkR32GN//O/voa2s2IT46Z1KFrBZP1FS4ub7B2d4/LfpGxZhQ64IIlHN49Ib/8HKMr2xy9exd/RiBfXWLRJcjtB6RrkeF2jbiygo0chTsj7dR57cbXOGpHHvz6d9wBtq1OOilBjOPHezAFcY6Hq8rO7hbJnX1OD58w3k1pzQupgCwJ3D2ldldY//KL7D13gh8xRVY6JIMxFCUPhwmDhYSFtGS1kePLEf5owr1fvsVwe4mTXpeN69dJ1ndpbl0CSclvf0jNCro43PIai0XFpN9HtM7R3iOSZkrPhOHjnEqblMNT9PFTmhd28DEE0iShmpRkFMRanXR+nlgZNi1Qg2qSsawtlnZfpLF7ifrGGtPFBTZfusrBb/9AdThEfGRYlTQaDcLgjDDKEKf0xNFsdQiNhHjQJZ+OCTFQDEc0L6zjtYoUWQ7OU4pRz3KqwYTp7jrHRPyHQzoqWF7hgrFxeZdkscNpIgxrgh0NSMtI7gJVCKgoiqAhYIkycCm0F4h1ZZw/gRgAKMqCVATvIgx7fXbWtslUaI9LxvtDyvU1jodDOoMCEaWX9yjvvY9+9C5XvvIKvt2ml2Ukd+4RmRKqCMHoD4fszC2jUmJVSU6D3umAfHpGnEyJFsnznMR58qLAFzjifp9i4wLtly4Tbt9nSQU7GZH1z/BZRObb1C9tcnTwgKWTU04fd+HCDiMi7ckp8w1oBkVU2Tt6SrG5RbLaIe8ds9hsk03HaMhJXaRVOU4aTdzuJr3DE9zrnZU31mpN+iGjtbtOe66FOUiLgnkTdHWBfHuFo7MR8uSYl2LCwmhE1usi0yk1AosKqSqunpKFklOJ7Oxs05jkNIKRhIo0cSQWaUwNLm/T3Wix/+5N5EdfvGGd1hwn2YiDNMKV51hbXKEeoI3nOJQ8OnjK8umYqy5lqcqJGgCPVRFxgnNCFEeRpjRyz1+zLtm1XZ5f30IeHtDcP6UxyTls1JDNVU5agVsf3Wbj8Rj56Suv2uraOr3uCeO8ZCSeMnWERkKmEZcbG9GzkyTUxSi9Yio0qkitqii8IyQpSRCiGa1x5FhL3mFAsbTA1tY6jUTxMTIsAqf9AeMnj9meBLYLh/z829+1kHpcFambknpPUCgsYl6ppSl1rwgFWILRBlW8r1CpiNERJUWtJCkqzrRCYyRMI3vFlBMXKJs1UIfLJvhJxnpMWIiOacsh45u3LA8VarNRICQzuaQGymw0NzVMIhodzmqz37mLmERmw6CCRJzB1EVcNHwFwTuiCVYZLgASQAwXobJInKv9HwgTmI1in4Ukg/+UZfIJv4g804b/HAz/y/app54D/7lT8A8hijL99C6y1wAAAABJRU5ErkJggg==",
      "s3_bucket": "sagemaker-us-east-1-974339051049",
      "s3_key": "test/bicycle_s_000030.png",
      "inferences": [
        0.24936507642269135,
        0.7506349086761475
      ]
    }
  }
}