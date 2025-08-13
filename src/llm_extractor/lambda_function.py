import json
import os
import boto3
import traceback
from datetime import datetime
from botocore.exceptions import ClientError
from botocore.config import Config
from ..common.aria_helper.mongo_utils import Mongo
from ..common.aria_helper.aria_utils import ARIA
from ..common.extraction_engine.strategy.ocr.full_page_ocr_extraction_engine import FullPageOCRExtractionEngine
from ..common.aria_helper.boto3_utils import get_secret, trigger_lambda

common_prefix = os.environ['COMMON_PREFIX']
llm_secret = get_secret(f'{common_prefix}-llm_params')
aria_environment = os.environ['ARIA_ENVIRONMENT']
mongo_uri = get_secret(f'{common_prefix}-mongodb_uri', return_json=False).strip('"')
aria_database = os.environ['ARIA_DATABASE']
process_name = os.environ['PROCESS_NAME']

aria_secret = get_secret(secret_name=f'{common_prefix}-aria_cm_tokens')


def check_if_valid(mongo_client, group, aria_wi_id, unique_id):
    error_message = ''

    # Unique combination for invoice
    filter = {"aria_wi_id": '', "vin": unique_id}
    mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'), collection_name="invoice")

    # Unique combination for bol
    if "bol" in group:
        filter = {"aria_wi_id": '', "attachment_id": unique_id}
        mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'), collection_name="bol")

    # Unique combination for title
    if "title" in group:
        filter = {"aria_wi_id": '', "title_id": unique_id}
        mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'), collection_name="title")

    entries_found = mongo_client.count_documents(data={"aria_wi_id": aria_wi_id})
    print("First entries found", entries_found)
    if entries_found == 0:

        entries_found = mongo_client.count_documents(data=filter)
        #  If 1
        if entries_found == 1:
            mongo_client.update_one(filter=filter,
                                    data={"$set": {"aria_wi_id": aria_wi_id, "updated_at": datetime.now()}})

        else:
            error_message = f'Number of entries found in the collection for this {filter} combination:' + str(
                entries_found)

    # wi repeated collection (this should not happen)
    elif entries_found > 1:
        error_message = 'Number of entries found in the collection for this aria_wi_id:' + str(entries_found)

    return error_message

def post_to_aria(bre_response, app_id, document_id):
    try:
        aria = ARIA(
            base_url=aria_secret[aria_environment]['url'],
            request_token=aria_secret[aria_environment]['token']
        )

        aria.bre_reply(
            app_id=app_id,
            item_id=document_id,
            bre_response=bre_response
        )
        return True
    except Exception as e:
        raise Exception(f"Failed to post to ARIA : {str(e)}")


def llm_extractor(event):
    body = event["body"]
    try:
        execution_id = ''
        # Init mongo
        mongo_client = Mongo(mongo_uri)
        mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'),
                                              collection_name="LLM_EXTRACTOR_COLLECTION")

        # Extracting data from input message
        now_in_ms = datetime.now()
        print(body)
        document = body.get('document', None)
        action = body.get('action', None)
        status = body.get('status', None)
        ocr_groups = document.get('ocr_groups', None)
        # group_name = ocr_groups[0]
        ocr_file = body.get('words_coordinates', None)
        execution_id = body.get('execution_id', None)
        retrys = event.get('retrys')

    except Exception as e:
        print('Bad request ({})'.format(e))
        mongo_client.insert_one(data={"execution_id": execution_id if execution_id else '',
                                      "time": now_in_ms.strftime("%m/%d/%Y-%H:%M:%S.%f"), "input": body,
                                      "success": False, "error_message": str(e)})
        mongo_client.close_connection()
        return {
            'statusCode': 400,
            'body': json.dumps('Bad request!')
        }

    try:
        # Checking if the current wi exists in data collection
        # error_message = check_if_valid(mongo_client, ocr_groups[0], document['id'], unique_id)
        # if error_message:
        #     print(error_message)
        #     mongo_client.close_connection()
        #     return {
        #         'statusCode': 500,
        #         'body': json.dumps(error_message)
        #     }
        mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'),
                                              collection_name="LLM_EXTRACTOR_COLLECTION")
        mongo_client.insert_one(
            data={"execution_id": execution_id, "time": now_in_ms.strftime("%m/%d/%Y-%H:%M:%S.%f"), "input": body,
                  "success": "", "error_message": ""})




        # Generating the json with expected format for BRE
        bre_input_json = {}
        bre_input_json['execution_id'] = execution_id
        bre_input_json['action'] = action
        bre_input_json['status'] = status
        bre_input_json['document'] = document

        # Operations at group level
        wi_fields_json_clean = {}
        for group_name in ocr_groups:
            print(f'Processing group:{group_name}')

            extraction_engine = FullPageOCRExtractionEngine(mongo_client,group_name)

            # Downloading ocr data
            link_to_download = ''
            if ocr_file.get(group_name, None):
                link_to_download = ocr_file.get(group_name, None)
            extraction_engine.get_ocr_data(link_to_download)

            # Processing the document in blocks of pages (as per classification)
            bre_fields_json, extracted_data_clean = extraction_engine.process_data(False, execution_id)
            wi_fields_json_clean[group_name] = extracted_data_clean
            bre_input_json['document']['groups'][group_name]['fields'].update(bre_fields_json)


        mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'), collection_name=group_name)
        mongo_client.update_one(filter={"aria_wi_id": document['id']},
                                data={"$set": {"extracted_data": wi_fields_json_clean, "updated_at": datetime.now()}})


        print('============bre_input_json===================')
        print(bre_input_json)
        print('===============================')

        trigger_lambda(f"{common_prefix}-{process_name}-bre_validation", {"body": bre_input_json})
        mongo_client.close_connection()

        return {
            'statusCode': 200,
            'body': json.dumps('Ok!')
        }

    except Exception as e:
        print('Error: {}'.format(traceback.format_exc()))
        aria_exception = ""
        bre_response = False
        if "Please reduce the length of the messages" in str(e):
            aria_exception = 'File too long to process'
            bre_response = True
        else:
            aria_exception = 'Exception extracting data'
            if retrys <= 0:
                bre_response = True
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps('LLM Error!')
                }

        if bre_response:
            try:
                # Extracting target status id
                for k, v in status.items():
                    if 'needs' in v['label'].lower():
                        target_status_label = v['label']
                        target_status_id = k
                        break
                try:
                    # Updating folios and llm_extractor collections with error
                    mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'),
                                                          collection_name=os.environ["LLM_EXTRACTOR_COLLECTION_NAME"])
                    mongo_client.update_one(filter={'execution_id': execution_id}, data={
                        "$set": {"success": False, "error_message": str(traceback.format_exc())}})
                except:
                    pass
                mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'),
                                                      collection_name=ocr_groups[0])
                note = datetime.now().strftime("%m/%d/%Y-%H:%M:%S") + '\n' + aria_exception
                mongo_client.update_one(
                    filter={"aria_wi_id": document['id']},
                    data={
                        "$set": {
                            "status": target_status_label,
                            "updated_at": datetime.now(),
                            "exception": aria_exception
                        },
                        "$push": {
                            "status_history": target_status_label
                        }
                    }
                )

                mongo_client.close_connection()



            except Exception as e:
                print('Error: {}'.format(traceback.format_exc()))

            return {
                'statusCode': 500,
                'body': json.dumps('Nok!')
            }


def lambda_handler(event, context):
    retrys = int(os.getenv("RETRYS", 3))
    finished_by_no_problem_with_llm = False

    while (finished_by_no_problem_with_llm == False and retrys > 0):
        event['retrys'] = retrys
        response = llm_extractor(event)
        if response['statusCode'] != 404:
            finished_by_no_problem_with_llm = True

        retrys -= 1
    return response