# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 13:35:52 2019

@license : CeCILL-2.1
@author: sebastien@gardoll.fr
"""

import yaml
import logging
import os


class YamlSerializable(yaml.YAMLObject):

    YAML_FILENAME_EXTENSION: str = 'yml'

    def __init__(self, str_id: str):
        self.str_id: str = str_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(str_id={self.str_id})"

        # Save this instance to the given path (override if it already exists)
    def save(self, file_path: str) -> None:
        try:
            logging.debug(f"saving {self.__class__.__name__} '{self.str_id}' to '{file_path}'")
            yml_content = yaml.dump(self, default_flow_style=False, indent=2)
        except Exception as e:
            logging.error(f"cannot serialize {self.__class__.__name__}: {str(e)}")
            raise e

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(yml_content)
        except Exception as e:
            logging.error(f"cannot save {self.__class__.__name__} to '{file_path}': {str(e)}")
            raise e

    @staticmethod
    def load(file_path: str) -> '? YamlSerializable':
        try:
            logging.debug(f"read file from '{file_path}'")
            with open(file_path, 'r') as file:
                yml_content = file.read()
        except Exception as e:
            logging.error(f"cannot open file '{file_path}': {str(e)}")
            raise e

        try:
            return yaml.load(yml_content, Loader=yaml.FullLoader)
        except Exception as e:
            logging.error(f"cannot deserialize: {str(e)}")
            raise e
