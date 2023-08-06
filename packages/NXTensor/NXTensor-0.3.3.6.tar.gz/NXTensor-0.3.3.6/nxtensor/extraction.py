#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:26:39 2019
@license : CeCILL-2.1
@author: sebastien@gardoll.fr
"""

from nxtensor.utils.time_resolutions import TimeResolution
from nxtensor.utils.csv_option_names import CsvOptName
from nxtensor.utils.db_types import DBType
from nxtensor.yaml_serializable import YamlSerializable
from nxtensor.variable import Variable
from nxtensor.core.types import VariableId, LabelId, DBMetadataMapping
import logging
from typing import List, Dict, Mapping


class ExtractionShape:

    SQUARE = 'square'


class ExtractionConfig(YamlSerializable):

    yaml_tag = u'ExtractionConfig'

    FILE_NAME_POSTFIX: str = 'extraction_config.yml'

    def compute_filename(self) -> str:
        return ExtractionConfig.generate_filename(self.str_id)

    @staticmethod
    def generate_filename(str_id: str) -> str:
        return f"{str_id}_{ExtractionConfig.FILE_NAME_POSTFIX}"

    # Because of None assignments.
    # noinspection PyTypeChecker
    def __init__(self, str_id: str):
        super().__init__(str_id)

        # Dask scheduler mode. See https://docs.dask.org/en/latest/scheduler-overview.html
        self.dask_scheduler: str = 'single-threaded'

        # x and y size of an image of the tensor.
        self.x_size: int = None
        self.y_size: int = None
        # Ordered list of variable file paths.
        self.variable_file_paths: List[str] = None
        # List of label file path descriptions.
        self.label_file_paths: List[str] = None
        self.extraction_shape: ExtractionShape = ExtractionShape.SQUARE
        # The path of required directories for an extraction and assemble (channel and tensor).
        self.qsub_log_dir_path: str = None
        self.blocks_dir_path: str = None
        self.channels_dir_path: str = None
        self.tensors_dir_path: str = None
        self.tmp_dir_path: str = None

        # The maximum number of process spawn during the extraction.
        # Each process treats one extraction_metadata_blocks.
        self.nb_process: int = None

        # The maximum walltime for the extraction per variable.
        self.max_walltime: str = None  # i.e. '01:59:59' hours:mins:seconds

        # The maximum memory foot print per process.
        self.extraction_mem_foot_print: str = None  # i.e. 10gb
        self.assembly_mem_foot_print: str = None  # i.e. 10gb

        # The number of processes and the number of extraction_metadata_blocks should be the same so
        # as to speed up the extraction. The less the number of extraction_metadata_blocks is, the greater
        # is the size of the extraction_metadata_blocks and the longer it takes to compute it.

        self.__variables: Dict[VariableId, Variable] = None  # Transient for yaml serialization.
        self.__labels: Dict[LabelId, ClassificationLabel] = None  # Transient for yaml serialization.

        # At the end of the tensor assemble. Has it to be shuffled ?
        self.has_tensor_to_be_shuffled: bool = None

        # The tensor will be split into the given dataset ratios.
        self.tensor_dataset_ratios: Mapping[str, float] = None

        # TODO: save metadata options (csv).

    def save(self, file_path: str) -> None:
        variables = self.__variables
        labels = self.__labels
        del self.__variables
        del self.__labels
        super().save(file_path)
        self.__variables = variables
        self.__labels = labels

    def get_variables(self) -> Mapping[VariableId, Variable]:
        variables_value = getattr(self, '__variables', None)
        if variables_value is None:
            logging.debug(f"loading the variables of {self.str_id}:")
            variables = list()
            for var_file_path in self.variable_file_paths:
                logging.debug(f"loading the variable {var_file_path}")
                var = Variable.load(var_file_path)
                variables.append(var)
            self.__variables: Dict[VariableId, Variable] = {var.str_id: var for var in variables}  # Preserve the order.

        return self.__variables

    def get_labels(self) -> Mapping[LabelId, 'ClassificationLabel']:
        labels_value = getattr(self, '__labels', None)
        if labels_value is None:
            logging.debug(f"loading the labels of {self.str_id}:")

            labels: ['ClassificationLabel'] = list()
            for label_file_path in self.label_file_paths:
                logging.debug(f"loading the label {label_file_path}")
                label = ClassificationLabel.load(label_file_path)
                labels.append(label)
            self.__labels = {label.str_id: label for label in labels}  # Preserve the order.

        return self.__labels


class ClassificationLabel(YamlSerializable):

    FILE_NAME_POSTFIX: str = 'label.yml'

    yaml_tag = u'ClassificationLabel'

    def compute_filename(self) -> str:
        return ClassificationLabel.generate_filename(self.dataset_id, self.str_id)

    @staticmethod
    def generate_filename(dataset_id: str, display_name: str) -> str:
        return f"{dataset_id}_{display_name}_{ClassificationLabel.FILE_NAME_POSTFIX}"

    # Because of None assignments.
    # noinspection PyTypeChecker
    def __init__(self, str_id: str, dataset_id: str):
        super().__init__(str_id)

        # Numerical str_id that encode the label.
        self.num_id: float = None
        # The dataset identifier.
        self.dataset_id: str = dataset_id
        # The path to the db that contains the information of the labels.
        self.db_file_path: str = None
        # The format of the data base of labels (CSV, etc.).
        self.db_format: DBType = None

        # The description of the db options (dictionary).
        self.db_open_options: Dict[CsvOptName, str] = None

        # Dictionary that maps required information about the labels:
        # convert keys (see enum_utils) into db column names.
        # noinspection PyTypeChecker
        self.db_meta_data_mapping: DBMetadataMapping = None

        # Time resolution in the db.
        self.db_time_resolution: TimeResolution = None

    def save(self, file_path: str) -> None:
        if CsvOptName.LINE_TERMINATOR in self.db_open_options:
            line_terminator = self.db_open_options[CsvOptName.LINE_TERMINATOR]
            if line_terminator == '\n':
                self.db_open_options[CsvOptName.LINE_TERMINATOR] = '\\n'
            super().save(file_path)
            self.db_open_options[CsvOptName.LINE_TERMINATOR] = line_terminator
        else:
            super().save(file_path)

    @staticmethod
    def load(file_path: str) -> 'ClassificationLabel':
        result = YamlSerializable.load(file_path)
        if CsvOptName.LINE_TERMINATOR in result.db_open_options:
            line_terminator = result.db_open_options[CsvOptName.LINE_TERMINATOR]
            if line_terminator == '\\n':
                result.db_open_options[CsvOptName.LINE_TERMINATOR] = '\n'
        return result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(str_id={self.str_id}, dataset_id={self.dataset_id}, " + \
               f"num_id={self.num_id}, db={self.db_file_path})"
