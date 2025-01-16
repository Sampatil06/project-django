def lambda_handler(event, context):
    try:
        num1 = event.get('num1')
        num2 = event.get('num2')

        if num1 is None or num2 is None:
            raise ValueError("Both 'num1' and 'num2' must be provided.")

        result = num1 + num2

        return {
            'statusCode': 200,
            'body': {
                'result': result
            }
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': {'error': str(e)}
        }
