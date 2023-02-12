import json

import main


def lambda_handler(event, context):

    main.main()

    return {
        'statusCode': 200,
        'body': json.dumps('Ran main.py!')
    }
