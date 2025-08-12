import os
import json

from ..common.validation_helper.validation_execution import ValidatorExecution
from ..common.aria_helper.boto3_utils import get_secret
from ..common.aria_helper.mongo_utils import Mongo
from ..common.aria_helper.aria_utils import ARIA

database_name = os.environ['DATABASE_NAME']
aria_environment = os.environ['ARIA_ENVIRONMENT']
common_prefix = os.environ['COMMON_PREFIX']
process_name = os.environ['PROCESS_NAME']


class BreValidationHandler:
    def __init__(self, event):
        self.event = event
        # Parse the event body once and reuse it
        self.document = event['body']["document"]
        self.input_body = self.document
        self.app_id = self.document['app_id']
        self.document_id = self.document['id']
        self.current_status_id = event['body']["action"]["source_status"]
        self.statuses = event['body']["status"]
        self.ocr_groups = self.document.get('ocr_groups', [])
        self.request_response = self.input_body.get('request_response', False)

        self.mongo_client = Mongo(get_secret(common_prefix + '-mongodb_uri', return_json=False)).client
        self.validator_execution = ValidatorExecution()
        self.aria_secret = get_secret(secret_name=f'{common_prefix}-aria_cm_tokens')
        self.validation_config = self.mongo_client[database_name][f"validation_config"].find_one({
            "app_id": self.app_id
        })

        if not self.validation_config:
            raise ValueError(f"No validation config found for app_id: {self.app_id}")

        if not self.app_id:
            raise ValueError("app_id is missing from the document")

    def post_to_aria(self, bre_response):
        try:
            aria = ARIA(
                base_url=self.aria_secret[aria_environment]['url'],
                request_token=self.aria_secret[aria_environment]['token']
            )

            aria.bre_reply(
                app_id=self.app_id,
                item_id=self.document_id,
                bre_response=bre_response
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to post to ARIA : {str(e)}")

    def run(self):
        try:
            # Perform validation
            is_valid, validation_result = self.validator_execution.validate_data(self.document, self.validation_config)
            aria_update_request = {k: v["fields"] for k, v in validation_result["groups"].items()}
            if is_valid:
                aria_update_request["aria_exception"] = {"value": ""}
            else:
                aria_update_request["aria_exception"] = {"value": validation_result.get('errors', "")}
                aria_update_request["aria_status"] = {"value": self.current_status_id}

            self.post_to_aria(aria_update_request)
            # Return response in the wanted format
            return {
                'statusCode': 200,
                'body': aria_update_request
            }

        except Exception as e:
            print('Error: {}'.format(str(e)))
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }


def lambda_handler(event, context=None):
    print("event-data", event)
    bre_validation_handler = BreValidationHandler(event)
    return bre_validation_handler.run()
