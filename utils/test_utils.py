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
    def get_datetime() -> str:
        """Şu anki tarih ve zamanı formatlanmış string olarak döndürür"""
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    @staticmethod
    def get_logger(class_name: str) -> logging.Logger:
        """Belirtilen sınıf için logger döndürür"""
        return logging.getLogger(class_name) 