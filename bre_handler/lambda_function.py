import os
import json
from ..common.aria_helper.crud_statuses import CrudStatuses
from ..common.aria_helper.crud_handler_execution import CrudHandler
from ..common.aria_helper.boto3_utils import trigger_lambda, trigger_lambda_response, get_secret
from ..common.aria_helper.mongo_utils import Mongo
from ..common.aria_helper.aria_utils import ARIA


database_name = os.environ['DATABASE_NAME']
aria_environment = os.environ['ENV']
common_prefix = os.environ['COMMON_PREFIX']
process_name = os.environ['PROCESS_NAME']


class BreHandler:
    def __init__(self, event):
        self.event = event
        self.input_body = json.loads(event['body'])
        self.action_data = self.input_body.get('action')
        self.document = self.input_body['document']
        self.app_id = self.document['app_id']
        self.statuses = self.input_body['status']
        self.mongo_client = Mongo(get_secret(common_prefix + '-mongodb_uri', return_json=False))
        self.aria_secret = get_secret(secret_name=f'{common_prefix}-aria_cm_tokens')
        self.crud_handler = CrudHandler(self.mongo_client)
        self.crud_statuses = CrudStatuses(self.mongo_client)
        self._set_llm_by_app_id()

    def _set_llm_by_app_id(self):
        self.mongo_client.select_db_and_collection(database_name, collection_name=f"llm_config")
        self.llm_by_app_id = self.mongo_client.find_one({"app_id": self.app_id})

    def handle_document_without_group(self):
        aria_exception = "No OCR. Cant execute bre rules"
        target_status_id = [k for k, v in self.statuses.items() if 'needs' in v['label'].lower()]
        if len(target_status_id) == 0:
            raise ValueError("No target status")
        aria = ARIA(base_url=self.aria_secret[aria_environment]['url'],
                    request_token=self.aria_secret[aria_environment]['token'])
        aria.bre_reply(
            app_id=self.document['app_id'],
            item_id=self.document['id'],
            bre_response={
                "aria_status": {"value": target_status_id},
                "aria_exception": {"value": aria_exception}
            })

    def next_step(self):
        next_function = None
        lambda_trigger_type = None
        bre_type = ""
        request_response = None
        action_name = self.action_data.get('action_label', None)
        if action_name:
            action_name = action_name.lower()

        print("ACTION TO DO", action_name)
        self.crud_statuses.insert_or_update(self.app_id, self.statuses)

        if action_name is None:
            print("Handling first-time processing")
            if len(self.document.get('ocr_groups', [])) == 0:
                self.handle_document_without_group()
                bre_type = "document_without_group"
            next_function = self.llm_by_app_id[self.app_id]
            lambda_trigger_type = trigger_lambda
            request_response = False

        else:
            self.mongo_client.select_db_and_collection(database_name, collection_name="action_config")
            actions_dict = self.mongo_client.find_one({"app_id": self.app_id})

            if action_name in actions_dict:
                action_vals = actions_dict[action_name]
                next_function = action_vals.get('next_function')
                request_response = action_vals.get('request_response')
                lambda_trigger_type = trigger_lambda_response if request_response else trigger_lambda

                if action_vals.get('request_response'):
                    bre_type = action_vals.get('bre_type')

        return bre_type, next_function, lambda_trigger_type, request_response

    def run(self):
        try:
            bre_type, next_function, method, request_response = self.next_step()

            if bre_type == "document_without_group":
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'No OCR to process'})
                }

            execution_id = self.crud_handler.insert_execution(self.input_body, next_function)

            self.input_body['bre_type'] = bre_type
            self.input_body['execution_id'] = execution_id
            self.input_body['request_response'] = request_response

            try:
                lambda_response = method(next_function, {"body":self.input_body})
            except Exception as e:
                self.crud_handler.mark_as_failed(execution_id, error_message=str(e))
                return {
                    'statusCode': 500,
                    'body': json.dumps({'message': 'Issue while triggering next lambda: ' + str(e)})
                }

            if method == trigger_lambda_response:
                response_payload = json.loads(lambda_response['Payload'].read())
                print("RESPONSE FROM LAMBDA ->> ", response_payload)

                return {
                    'statusCode': response_payload.get('statusCode'),
                    'body': response_payload.get('body')
                }

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Working on it'})
            }

        except Exception as e:
            self.crud_handler.insert_execution(self.event, 'None', failed=True, error_message=str(e))
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Issue while processing the petition: ' + str(e)})
            }


def lambda_handler(event, context):
    if 'body' not in event:
        raise ValueError("body tag is missing on the dict. Skipping...")

    bre_handler = BreHandler(event)
    return bre_handler.run()