import boto3
import json
import logging
import os
import csv

from botocore.exceptions import ClientError

BUCKET_NAME=os.environ['BUCKET_NAME']

s3 = boto3.resource('s3')

def FetchFileFromS3(fileName):
    try:
        obj = s3.Object(BUCKET_NAME, fileName)
        body = obj.get()['Body'].read()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return []
        else:
            logging.error(e.response)
            raise Exception(e)
    except Exception as e:
        logging.error(e)
        raise Exception(e)

    return toArray(body.decode('utf-8'))


def toArray(obj):
    history = []
    rows = obj.split('\n')
    for row in rows:
        try:
            data = row.split(',')
            history.append((data[0], data[1]))
        except IndexError as e:
            break

    return history


def WriteFileToS3(array, fileName):
    m = ''
    for his in array:
        m += f'{his[0]}, {his[1]}\n'
    obj = s3.Object(BUCKET_NAME, fileName)
    response = obj.put(
        Body=m.encode('utf-8'),
        ContentEncoding='utf-8',
        ContentType='text/csv'
    )


# FetchFileFromS3('cointelegraph.csv')
