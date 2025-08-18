import os
import json
from typing import Dict, Any

from ..common.validation_helper.validation_execution import ValidatorExecution
from ..common.aria_helper.boto3_utils import get_secret
from ..common.aria_helper.mongo_utils import Mongo
from ..common.aria_helper.aria_utils import ARIA

database_name = os.environ.get('DATABASE_NAME')
aria_environment = os.environ.get('ARIA_ENVIRONMENT')
common_prefix = os.environ.get('COMMON_PREFIX')
process_name = os.environ.get('PROCESS_NAME')


class BreValidationHandler:
    """
    This class encapsulates the business logic for the validation process,
    based on your original file structure.
    """
    def __init__(self, event: Dict[str, Any]):
        self.event = event
        
        self.document = event['body']["document"]
        self.input_body = self.document
        self.app_id = self.document['app_id']
        self.document_id = self.document['id']
        
        
        self.source_status_id = event['body']["action"]["source_status"]
        self.target_status_id = event['body']["action"]["target_status"]

        self.statuses = event['body']["status"]
        self.ocr_groups = self.document.get('ocr_groups', [])
        self.request_response = self.input_body.get('request_response', False)

        # Initialize clients and configurations
        self.mongo_client = Mongo(get_secret(f'{common_prefix}-mongodb_uri', return_json=False)).client
        self.validator_execution = ValidatorExecution() # Correct class name
        self.aria_secret = get_secret(secret_name=f'{common_prefix}-aria_cm_tokens')
        self.validation_config = self.mongo_client[database_name][f"validation_config"].find_one({
            "app_id": self.app_id
        })

        if not self.validation_config:
            raise ValueError(f"No validation config found for app_id: {self.app_id}")

        if not self.app_id:
            raise ValueError("app_id is missing from the document")

    def post_to_aria(self, bre_response: Dict[str, Any]):
        """Posts the validation result back to the ARIA system."""
        try:
            print(f"Posting to ARIA for document_id: {self.document_id}")
            aria = ARIA(
                base_url=self.aria_secret[aria_environment]['url'],
                request_token=self.aria_secret[aria_environment]['token']
            )

            aria.bre_reply(
                app_id=self.app_id,
                item_id=self.document_id,
                bre_response=bre_response
            )
            print(f"Successfully posted to ARIA for document_id: {self.document_id}")
            return True
        except Exception as e:
            # Provide a more detailed error log if the post fails
            print(f"ERROR: Failed to post to ARIA for document_id {self.document_id}. Reason: {str(e)}")
            raise Exception(f"Failed to post to ARIA : {str(e)}")

    def run(self) -> Dict[str, Any]:
        """Executes the main validation and status update logic."""
        try:
            print(f"Starting validation for document_id: {self.document_id}")
            # Perform validation
            is_valid, validation_result = self.validator_execution.validate_data(self.document, self.validation_config)
            
            # Prepare the payload for the ARIA system
            aria_update_request = {k: v["fields"] for k, v in validation_result["groups"].items()}
            
            if is_valid:
                print(f"Validation successful for document_id: {self.document_id}")
                aria_update_request["aria_exception"] = {"value": ""}
                # Note: If valid, the status progresses automatically in ARIA based on the workflow.
                # We don't need to set a status here.
            else:
                print(f"Validation failed for document_id: {self.document_id}")
                aria_update_request["aria_exception"] = {"value": validation_result.get('errors', "")}
                
                # (DEFINITIVE FIX) Set the status to the correct 'target_status' (e.g., "Needs Attention")
                # instead of the old 'source_status' ("Loading").
                aria_update_request["aria_status"] = {"value": self.target_status_id}

            # Post the results back to update the status
            self.post_to_aria(aria_update_request)
            
            # Return a success response
            return {
                'statusCode': 200,
                'body': json.dumps(aria_update_request)
            }

        except Exception as e:
            print(f'CRITICAL ERROR during run for document_id {self.document_id}: {str(e)}')
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Main entry point for the Lambda function.
    """
    print("Received event data:", event)
    try:
        
        from ..common.validation_helper.validation_execution import ValidatorExecution
        
        bre_validation_handler = BreValidationHandler(event)
        return bre_validation_handler.run()
    except Exception as e:
        # Catch initialization errors 
        print(f"Failed to initialize BreValidationHandler. Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Initialization failed: {str(e)}"})
        }
