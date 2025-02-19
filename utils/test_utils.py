import logging
import datetime
import xml.etree.ElementTree as ET
from typing import Dict

class TestUtils:
    WAIT = 10  # Default wait time
    
    @staticmethod
    def parse_string_xml(file_path: str) -> Dict[str, str]:
        """XML dosyasını parse eder ve bir dictionary olarak döndürür"""
        string_map = {}
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for elem in root.findall(".//string"):
            string_map[elem.get("name")] = elem.text
            
        return string_map
    
    @staticmethod
    def get_current_timestamp() -> str:
        """Returns the current timestamp in the format YYYY-MM-DD-HH-MM-SS"""
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    @staticmethod
    def get_logger(class_name: str) -> logging.Logger:
        """Returns a logger for the specified class"""
        return logging.getLogger(class_name) 