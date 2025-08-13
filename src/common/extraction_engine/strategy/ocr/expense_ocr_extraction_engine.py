from ..ocr_extraction_engine_abs import OCRExtractionEngine


class ExpenseOCRExtractionEngine(OCRExtractionEngine):

    def __init__(self):
        self.ocr_per_page_block = None
        self.total_pages = None
        self.ocr_per_line_per_page_plain = {}
        self.ocr_per_page_plain = {}
        self.ocr_per_page_dict_with_coords = {}
        self.ocr_per_page_dict = {}
        self.ids_to_page_mapping = {}
        self.ids_to_coord_mapping = {}

    def get_ocr_data(self, link_to_download):
        pass


    def classify_page(self):
        pass

    def process_data(self, classify_needed:bool, execution_id: str):
        pass
