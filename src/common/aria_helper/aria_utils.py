import requests


class ARIA:

    def __init__(self, base_url, request_token):
        self.headers = {'Authorization': request_token, 'Content-Type': 'application/json',
                        'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br'}
        self.base_url = base_url

    def _request_to_aria(self, request_type, url, body):
        if request_type == 'post':
            response = requests.post(url, json=body, headers=self.headers)
        elif request_type == 'get':
            response = requests.get(url, headers=self.headers)
        else:
            raise TypeError('Type not supported!')

        if response.status_code != 202:
            print(response.status_code)

    def bre_reply(self, app_id, item_id, bre_response):
        url = f'{self.base_url}/public/v1/apps/{app_id}/case_management_middleware/work_items/{item_id}/bre'
        body = {
            "data": {
                "type": "workItem",
                "id": item_id,
                "attributes": {
                    "response": bre_response
                }
            }
        }
        self._request_to_aria('post', url, body)

    def create_item(self, group_name, pdf_base64, app_id):
        url = f'{self.base_url}/public/v1/apps/{app_id}/document_processing'
        body = {
            "data": {
                "attributes": {
                    "groups": [
                        {
                            "name": group_name,
                            "content": f"data:application/pdf;base64,{pdf_base64}",

                            "metadata": []
                        }

                    ]
                },
                "type": "CaseManagement"
            }
        }
        self._request_to_aria('post', url, body)

    def create_event(self, app_id, item_id, title, body=None, status=None):
        url = f'{self.base_url}/public/v1/apps/{app_id}/case_management_middleware/work_items/{item_id}/events'
        request_body = {
            "data": {
                "type": "event",
                "attributes": {
                    "title": title
                }
            }
        }

        if body:
            request_body['data']['attributes']['body'] = body

        if status is not None:
            status_code = 'Completed' if status == 0 else ('Failed' if status == 1 else 'Warning')
            request_body['data']['attributes']['status'] = status_code

        self._request_to_aria('post', url, request_body)
