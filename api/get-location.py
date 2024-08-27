import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def lambda_handler(event, context):
    address = str(event.get('address', ""))
    address = address.replace("-", "")
    if not address:
        return {
            'input': address,
            'statusCode': 400,
            'body': json.dumps('Error: No address provided')
        }
    
    try:
        # Create a client for Amazon Location Service
        client = boto3.client('location', region_name='eu-west-1')

        # Perform the geocoding request
        response = client.search_place_index_for_text(
            IndexName='GetLocation',
            Text=address
        )

        # Extract coordinates from the response
        if 'Results' in response and len(response['Results']) > 0:
            result = response['Results'][0]
            coordinates = result['Place']['Geometry']['Point']
            
            return {
                'statusCode': 200,
                'body': coordinates
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps('No coordinates found for the provided address')
            }

    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: AWS credentials not found')
        }
    except PartialCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: Incomplete AWS credentials')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
