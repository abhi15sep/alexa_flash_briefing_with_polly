# coding=utf-8

import os
import json
import boto3
from boto3 import Session
from boto3 import resource
from contextlib import closing


AUDIO_BUCKET = os.environ["AUDIO_BUCKET"]
session = Session(region_name="us-east-1")
polly = session.client("polly")
s3 = boto3.resource('s3')
bucket = s3.Bucket(AUDIO_BUCKET)

def create_audio(events):
    for event in events:
        print("mainText: {}".format(event["mainText"]))
        response = polly.synthesize_speech(
                Text=event["mainText"],
                OutputFormat="mp3",
                VoiceId="Mizuki")
        with closing(response["AudioStream"]) as stream:
            key_name = "{}.mp3".format(event["uid"])
            print("store to -> {}".format(key_name))
            bucket.put_object(
                Key=key_name,
                Body=stream.read(),
                ACL="public-read")

def lambda_handler(event, context):

    print(event)
    if len(event) > 0:
        create_audio(event)

    return True
