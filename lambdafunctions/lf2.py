import json
import boto3

def lex_handler(message):
    lex_cli = boto3.client('lexv2-runtime')    

    BOT_ID = os.environ['BOT_ID']
    BOT_ALIAS_ID = os.environ['BOT_ALIAS_ID']
    LOCALE_ID = os.environ['LOCALE_ID']

    lex_response = lex_cli.recognize_text(
        botId=BOT_ID,
        botAliasId=BOT_ALIAS_ID,
        localeId=LOCALE_ID,
        sessionId='test_session',
        text=q1
    )
    print(lex_response)

    if lex_response['sessionState']['intent']['slots'] == {}:
        print("No slots")
    else:
        slots = lex_response['sessionState']['intent']['slots']['PhotoType']['value']['originalValue']
        print(slots)

def lambda_handler(event, context):
    # TODO implement
    q1 = event['queryStringParameters']['q']

    lex_handler(q1)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
