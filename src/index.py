import boto3
import json
import logging
import os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from coinmarketcap import CoinMarketCap
 
# CoinTelegraph
# CoinDesk
# CryptoNews
# CCN

# HOOK_URL = os.environ['hookUrl']
# SLACK_CHANNEL = os.environ['slackChannel']

HOOK_URL = 'https://hooks.slack.com/services/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'
SLACK_CHANNEL = 'report-test'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    sendToSlack(CoinMarketCap(HOOK_URL, SLACK_CHANNEL))
    


def sendToSlack(message):
    req = Request(HOOK_URL, json.dumps(message).encode('utf-8'))

    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", message['channel'])
    except HTTPError as e:
        logger.info("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.info("Server connection failed: %s", e.reason)


lambda_handler('', '')