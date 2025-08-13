from abc import abstractmethod
from typing_extensions import override
from .extraction_engine_abs import ExtractionEngine


class OCRExtractionEngine(ExtractionEngine):

    @override
    def start_engine(self):
        pass

    @abstractmethod
    def get_ocr_data(self, link_to_download):
        raise NotImplemented("This method must be implemented in subclass")

    @abstractmethod
    def process_data(self, classify_needed: bool, execution_id: str):
        raise NotImplemented("This method must be implemented in subclass")
