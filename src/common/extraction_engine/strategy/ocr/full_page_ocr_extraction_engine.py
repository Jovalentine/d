import traceback
from collections import defaultdict
from typing import Any
from ..ocr_extraction_engine_abs import OCRExtractionEngine
import requests
import json
from dataclasses import dataclass
import os
from ....llm_helper.llm_factory import LLMModelFactory
from ....llm_helper.llm_models import LLMModel
import re
from ....aria_helper.boto3_utils import get_secret
from ...prompts import extraction_prompt, date_transformer, coord_prompt
from ...fields_to_extract import fields, fields_json, fields_json_v2, fields_type

common_prefix = os.environ['COMMON_PREFIX']


@dataclass
class FullPageOCRExtractionEngine(OCRExtractionEngine):
    mongo_client: Any
    group_name: str
    llm_factory = LLMModelFactory()

    def __post_init__(self):
        if not self.mongo_client:
            raise ValueError('mongo_client is not set while creating the engine')
        self.group_pages_list = None
        self.ocr_per_page_block = []  # contains all test id and page
        self.total_pages = None
        self.ocr_per_line_per_page_plain = defaultdict(str)  # contains lines for each page
        self.ocr_per_page_plain = defaultdict(str)  # contains text for each page
        self.ocr_per_page_dict_with_coords = defaultdict(list)  # contains text id with coords for each page
        self.ocr_per_page_dict = defaultdict(list)  # text with id for each page
        self.ids_to_page_mapping = {}  # This is to store id and coordinates
        self.ids_to_coord_mapping = {}  # This is to store id and coordinates

    def get_used_llm_dict(self):
        llm_secret = get_secret(f'{common_prefix}-llm_params')
        return {
            "gpt": self.llm_factory.get_llm_model(LLMModel.OPENAI, llm_secret['openai']['public']['gpt4o']['llm_params']),
            "gpt_mini": self.llm_factory.get_llm_model(LLMModel.OPENAI,
                                                       llm_secret['openai']['public']['gpt4o3-mini']['llm_params']),
            "aux1": self.llm_factory.get_llm_model(LLMModel.BEDROCK,
                                                   llm_secret['bedrock']['claude']['claude3.7-sonnet']['llm_params']),
            "aux2": self.llm_factory.get_llm_model(LLMModel.BEDROCK,
                                                   llm_secret['bedrock']['claude']['claude3.5-sonnet']['llm_params']),
        }

    def get_ocr_data(self, link_to_download):
        r = requests.get(link_to_download)
        ocr_data = json.loads(r.content.decode('utf-8'))
        self.total_pages = ocr_data['DocumentMetadata']['Pages']
        word_id = 1
        for block in ocr_data['Blocks']:
            if block['BlockType'] == 'WORD':
                page_nr = int(block['Page']) - 1
                self.ids_to_coord_mapping[str(word_id)] = block['Geometry']
                self.ids_to_page_mapping[str(word_id)] = page_nr
                self.ocr_per_page_dict[page_nr].append({'Text': block['Text'], 'Id': str(word_id)})
                self.ocr_per_page_block.append({'Text': block['Text'], 'Id': str(word_id), 'Page': block['Page']})
                self.ocr_per_page_plain[page_nr] += block['Text'] + ' '
                self.ocr_per_page_dict_with_coords[page_nr].append(
                    {'Text': block['Text'], 'Id': str(word_id), 'Coords': str(block['Geometry']['Polygon'])})
                word_id += 1
            elif block['BlockType'] == 'LINE':
                page_nr = int(block['Page']) - 1
                self.ocr_per_line_per_page_plain[page_nr] += block['Text'] + '\n'

    def page_groups_generator(self, classify_needed: bool):
        if not classify_needed:
            yield range(self.total_pages)
        else:
            for i in range(0, self.total_pages, 10):
                yield range(i, min(i + 10, self.total_pages))

    def process_data(self, classify_needed, execution_id: str):
        for index, page_range in enumerate(self.page_groups_generator(classify_needed)):
            raw_text_ocr = [self.ocr_per_page_dict[page] for page in page_range]
            raw_text_plain = ''.join([self.ocr_per_page_plain[page] for page in page_range])

            to_extract = fields[self.group_name]
            self.llms_wapper_map = self.get_used_llm_dict()

            # Calling GPT to extract data
            message = f"""Extract the following: \n{to_extract} \n\n from the following text: \n{raw_text_ocr}\n\nThis is the previous text split by lines:\n"""
            message_without_ids = f"""Extract the following: \n{to_extract} \n\n from the following text: \n{raw_text_plain}\n\nThis is the previous text split by lines:\n"""
            for page in page_range:
                message += "\n".join(self.ocr_per_line_per_page_plain[page].split("\n")) + "\n"
                message_without_ids += "\n".join(self.ocr_per_line_per_page_plain[page].split("\n")) + "\n"

            gpt_output = self.llms_wapper_map['gpt'].send_message_to_llm(
                prompt=extraction_prompt.replace("{json}", json.dumps(fields_json[self.group_name])),
                message=message)

            self.mongo_client.select_db_and_collection(db_name=os.environ.get('DATABASE_NAME'),
                                                       collection_name=os.environ["LLM_EXTRACTOR_COLLECTION_NAME"])
            self.mongo_client.update_one(filter={'execution_id': execution_id},
                                         data={"$set": {f"{self.group_name}.extracted_data_gpt4": gpt_output}})
            return self.validate_gpt_output(index, gpt_output, message_without_ids, execution_id, raw_text_ocr, to_extract)

    def recursive_validation(self, message_without_ids, execution_id):
        llm_call_error = True
        retry_calling = 1
        claude_output = None
        llama3_output = None
        while llm_call_error == True and retry_calling > 0:
            try:
                # Calling Claude3 Haiku to extract data
                claude_output = self.llms_wapper_map['aux1'].send_message_to_llm(
                    prompt=extraction_prompt.replace("{json}", json.dumps(fields_json_v2[self.group_name])),
                    message=message_without_ids)
                self.mongo_client.update_one(filter={'execution_id': execution_id},
                                             data={
                                                 "$set": {f"{self.group_name}.extracted_data_claude3": claude_output}})

                # Calling Llama3 8b to extract data
                llama3_output = self.llms_wapper_map['aux2'].send_message_to_llm(
                    prompt=extraction_prompt.replace("{json}", json.dumps(fields_json_v2[self.group_name])),
                    message=message_without_ids)
                self.mongo_client.update_one(filter={'execution_id': execution_id},
                                             data={"$set": {f"{self.group_name}.extracted_data_llama3": llama3_output}})

                llm_call_error = False

            except Exception as e:
                llm_call_error = True
                retry_calling -= 1
        return claude_output, llama3_output

    def date_transformer(self, bre_fields_json):
        try:
            # Extracting the fields with dates
            date_fields_list = [x.lower().replace(' ', '_') for x in fields[self.group_name] if 'date' in x]
            if date_fields_list:
                date_fields_json = {}
                for field in date_fields_list:
                    if bre_fields_json.get(field, None):
                        date_fields_json[field] = bre_fields_json.get(field)
                # Transforming dates into american format
                date_fields_json = self.llms_wapper_map['gpt'].send_message_to_llm(prompt=date_transformer,
                                                                                   message=f"""Here you have the json: \n{date_fields_json} \n\n Just provide the transformed json as output.""")
                # Merging the transformed dates into original json
                if(isinstance(date_fields_json,str)):
                    date_fields_json = json.loads(date_fields_json)
                for field in date_fields_list:
                    if date_fields_json.get(field, None):
                        bre_fields_json[field] = date_fields_json.get(field)
        except Exception as e:
            print('Issue while operating dates: {}'.format(traceback.format_exc()))

    def validate_gpt_output(self, index, gpt_output, message_without_ids, execution_id, raw_text_ocr, to_extract):
        llm_call_error = True
        global_bre_fields_json = {}
        claude_output, llama3_output = self.recursive_validation(message_without_ids, execution_id)
        id_regex = "\[Id: '([0-9a-z-]*)']"
        if not llm_call_error:
            # Cleaning GPT json
            gpt_output_clean = {}
            for k, v in gpt_output.items():
                if isinstance(v, dict):
                    gpt_output_clean[k] = json.loads(re.sub(id_regex, '', json.dumps(v)))
                else:
                    gpt_output_clean[k] = re.sub(id_regex, '', v)

            fields_ok, fields_nok = self.validate_extracted_data(gpt_output_clean, claude_output, llama3_output)

            self.mongo_client.update_one(filter={'execution_id': execution_id}, data={
                "$set": {f"{self.group_name}.fields_ok": fields_ok, f"{self.group_name}.fields_nok": fields_nok}})

            if fields_nok:
                gpt_output2 = self.llms_wapper_map['gpt'].send_message_to_llm(
                    prompt=extraction_prompt.replace("{json}", json.dumps(fields_json[self.group_name])),
                    message=f"""Extract the following: \n{to_extract} \n\n from the following text: \n{raw_text_ocr}\n\n\n\nUse these values extracted by other LLM as reference:\n{claude_output}""")

                for field in fields_nok:
                    gpt_output[field] = gpt_output2[field]

            self.mongo_client.update_one(filter={'execution_id': execution_id},
                                         data={"$set": {f"{self.group_name}.extracted_data_gpt4_final": gpt_output}})

        bre_fields_json = self.extract_field_values_and_coordinates(gpt_output, id_regex,
                                                                    self.llms_wapper_map["gpt_mini"])

        # Dates operations (optional)
        self.date_transformer(bre_fields_json)
        global_bre_fields_json[index] = bre_fields_json
        print(global_bre_fields_json,"global_bre_fields_json")
        bre_fields_json = global_bre_fields_json[0]

        extracted_data_clean = defaultdict(dict)
        for field, value in bre_fields_json.items():
            if isinstance(value['value'], str):
                extracted_data_clean[field] = re.sub(id_regex, '', value['value']).rstrip() if not isinstance(
                    value['value'], bool) else value['value'].rstrip()
            else:
                for kk, vv in value['value'].items():
                    for kkk, vvv in vv['cells'].items():
                        extracted_data_clean[field][str(kk)][kkk] = vvv['value'].rstrip() if not isinstance(
                            vvv['value'], bool) else vvv['value'].rstrip()

        return bre_fields_json, extracted_data_clean

    def validate_extracted_data(self, main_data, validation_data1, validation_data2):
        """
        This method will apply the following validation matrix:

            GPT4 = A    | Claude = A    | Llama = A     --> Output = A
            GPT4 = A    | Claude = A    | Llama = B     --> Output = A
            GPT4 = A    | Claude = B    | Llama = C     --> Output = A
            GPT4 = A    | Claude = none | Llama = none  --> Output = A
            GPT4 = A    | Claude = B    | Llama = B     --> Output = repeat call to GPT
            GPT4 = none | Claude = A    | Llama = A     --> Output = repeat call to GPT
            GPT4 = none | Claude = none | Llama = none  --> Output = nope
        """
        fields_ok, fields_nok = [], []
        for k, v in main_data.items():
            main_value = re.sub(" |[$]", "", str(v).lower())
            validation_value1 = re.sub(" |[$]", "", str(validation_data1.get(k, 'NONE')).lower())
            validation_value2 = re.sub(" |[$]", "", str(validation_data2.get(k, 'NONE')).lower())

            if main_value == validation_value1 == validation_value2 or \
                    validation_value1 != validation_value2 or \
                    validation_value1 == validation_value2 == 'none':
                fields_ok.append(k)
            else:
                fields_nok.append(k)
        return fields_ok, fields_nok

    def extract_field_values_and_coordinates(self, gpt_output, id_regex, llm_wrapper_gpt):
        bre_fields_json = {}
        gpt_output = json.loads(gpt_output)
        print(gpt_output,type(gpt_output),"gpt_output===")
        for field, value in gpt_output.items():
            try:
                original_field = field
                coords = None
                field = field.lower().replace(' ', '_')
                # Regular field (plain text)
                if fields_type[self.group_name][original_field].get('type', None) == 'regular' and isinstance(
                        gpt_output[original_field], str):
                    if value.lower() == 'none':
                        continue

                    id_founds = re.findall(id_regex, value)

                    if len(id_founds) == 0:
                        pass

                    elif len(id_founds) == 1:
                        coords = self.ids_to_coord_mapping[id_founds[0]]
                        print(coords,"coords")
                    #  If multi-word value, we ask GPT to generate the surrounding box containing all the words
                    else:
                        c = 1
                        coords = ''
                        for id in id_founds:
                            coords += """
                                Word{}:
                                x={}
                                y={}
                                width={}
                                height={}

                            """.format(c, self.ids_to_coord_mapping[id]['Polygon'][0]['X'],
                                       self.ids_to_coord_mapping[id]['Polygon'][0]['Y'],
                                       self.ids_to_coord_mapping[id]['BoundingBox']['Width'],
                                       self.ids_to_coord_mapping[id]['BoundingBox']['Height'])
                            c += 1
                        coord_gpt_output = llm_wrapper_gpt.send_message_to_llm(prompt='You are a helpful AI assistant',
                                                                    message=coord_prompt.replace("{coords}", coords))
                        print(coord_gpt_output,"coord_gpt_output")
                        if isinstance(coord_gpt_output,str):
                            coord_gpt_output = json.loads(coord_gpt_output)
                    # Building JSON using Case Manager expected format
                    bre_fields_json[field] = {
                        "value": re.sub(id_regex, '', value).rstrip(),
                        "coordinates": {
                            "x": coords['Polygon'][0]['X'] if len(id_founds) == 1 else coord_gpt_output['x'],
                            "y": coords['Polygon'][0]['Y'] if len(id_founds) == 1 else coord_gpt_output['y'],
                            "width": coords['BoundingBox']['Width'] if len(id_founds) == 1 else coord_gpt_output[
                                'width'],
                            "height": coords['BoundingBox']['Height'] if len(id_founds) == 1 else coord_gpt_output[
                                'height'],
                            "page": self.ids_to_page_mapping[id_founds[0]] + 1
                        } if len(id_founds) > 0 else {},
                        "pass": True,
                        "display": True,
                        "message": ""
                    }
                else:
                    print('Unexpected field type extracted by LLM ({} vs {})'.format(type(gpt_output[original_field]),
                                                                                     fields_type[self.group_name][
                                                                                         original_field].get('type',
                                                                                     None)))
            except Exception as e:
                print(f"ERROR: {traceback.format_exc()}")
                continue
        return bre_fields_json
