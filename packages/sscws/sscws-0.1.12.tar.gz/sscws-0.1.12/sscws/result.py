#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2013-2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module defining classes to represent the Result class and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Callable, Dict, List
from abc import ABCMeta, abstractmethod
from enum import Enum
import dateutil.parser
import numpy as np

from sscws import ET_NS
from sscws.coordinates import CoordinateSystem
from sscws.regions import FootpointRegion, Hemisphere, SpaceRegion


class ResultStatusCode(Enum):
    """
    Enumerations representing the ResultStatusCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    CONDITIONAL_SUCCESS = 'ConditionalSuccess'
    ERROR = 'Error'


class ResultStatusSubCode(Enum):
    """
    Enumerations representing the ResultStatusSubCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    MISSING_REQUEST = 'MissingRequest'
    MISSING_SATELLITES = 'MissingSatellites'
    INVALID_BEGIN_TIME = 'InvalidBeginTime'
    INVALID_END_TIME = 'InvalidEndTime'
    INVALID_SATELLITE = 'InvalidSatellite'
    INVALID_TIME_RANGE = 'InvalidTimeRange'
    INVALID_RESOLUTION_FACTOR = 'InvalidResolutionFactor'
    MISSING_OUTPUT_OPTIONS = 'MissingOutputOptions'
    MISSING_COORD_OPTIONS = 'MissingCoordOptions'
    MISSING_COORD_SYSTEM = 'MissingCoordSystem'
    INVALID_COORD_SYSTEM = 'InvalidCoordSystem'
    MISSING_COORD_COMPONENT = 'MissingCoordComponent'
    MISSING_GRAPH_OPTIONS = 'MissingGraphOptions'
    MISSING_COORDINATE_SYSTEM = 'MissingCoordinateSystem'
    MISSING_COORDINATE_COMPONENT = 'MissingCoordinateComponent'
    SERVER_ERROR = 'ServerError'


class Result(metaclass=ABCMeta):
    """
    Class representing a Result from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Notes
    -----
    Although this class is essentially a dictionary, it was defined as a
    class to make certain that it matched the structure and key names
    of a Request from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    It also needs to function as a base class for the concrete
    sub-classes of a Request.

    Properties
    ----------
    status_code
        Result status code.
    status_sub_code
        Result status sub-code.
    status_text
        Result status text.
    """
    @abstractmethod
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str]):
        """
        Creates an object representing a Result from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        status_code
            Result status code value.
        status_sub_code
            Result status subcode value.
        status_text
            Status text.
        """
        self._status_code = status_code
        self._status_sub_code = status_sub_code
        self._status_text = status_text


    @property
    def status_code(self):
        """
        Gets the status_code value.

        Returns
        -------
        str
            status_code value.
        """
        return self._status_code


    @status_code.setter
    def status_code(self, value):
        """
        Sets the status_code value.

        Parameters
        ----------
        value
            status_code value.
        """
        self._status_code = value



    @property
    def status_sub_code(self):
        """
        Gets the status_sub_code value.

        Returns
        -------
        str
            status_sub_code value.
        """
        return self._status_sub_code


    @status_sub_code.setter
    def status_sub_code(self, value):
        """
        Sets the status_sub_code value.

        Parameters
        ----------
        value
            status_sub_code value.
        """
        self._status_sub_code = value



    @property
    def status_text(self):
        """
        Gets the status_text value.

        Returns
        -------
        str
            status_text value.
        """
        return self._status_text


    @status_text.setter
    def status_text(self, value):
        """
        Sets the status_text value.

        Parameters
        ----------
        value
            status_text value.
        """
        self._status_text = value


    @staticmethod
    def get_result(
            result_element: ET
        ) -> Dict:
        """
        Produces a Result from the given xml representation of a Result.

        Parameters
        ----------
        result_element
            ElementTree representation of a Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree Result
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of Result.
        """

        result_type = result_element.get(\
            '{http://www.w3.org/2001/XMLSchema-instance}type')

        if result_type == 'DataResult':
            return Result.get_data_result(result_element)

        if result_type == 'FileResult':
            return Result.get_file_result(result_element)

        raise ValueError('Unrecognized Result type = ' + result_type)


    @staticmethod
    def get_status(
            result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a Result with the StatusCode and
        SubStatusCode values from the given xml representation of a Result.

        Parameters
        ----------
        result_element
            ElementTree representation of a Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree Result
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            containing the StatusCode and SubStatusCode values.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            DataResult.
        """

        # should these be string or enum values ???
        return {
            'StatusCode': result_element.find(ET_NS + 'StatusCode').text,
            'StatusSubCode': result_element.find(\
                   ET_NS + 'StatusSubCode').text
        }


    @staticmethod
    def get_data_result(
            data_result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a DataResult from the given
        xml representation of a DataResult.

        Parameters
        ----------
        data_result_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree DataResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            DataResult.
        """

        result = Result.get_status(data_result_element)

        data_elements = data_result_element.findall(ET_NS + 'Data')
        data_len = len(data_elements)
        if data_len > 0:
            result['Data'] = np.empty(data_len, dtype=object)

            for data_i, data_element in enumerate(data_elements):

                coords_element = data_element.find(ET_NS + 'Coordinates')

                if coords_element is None:
                    # Is this the correct result for this case???
                    result['Data'][data_i] = {
                        'Id': data_element.find(ET_NS + 'Id').text
                    }
                    continue

                result['Data'][data_i] = {
                    'Id': data_element.find(ET_NS + 'Id').text,
                    'Coordinates': {
                        'CoordinateSystem': CoordinateSystem(\
                            coords_element.find(\
                                ET_NS + 'CoordinateSystem').text),
                    },
                }


                for name in ['X', 'Y', 'Z', 'Latitude', 'Longitude',
                             'LocalTime']:
                    result['Data'][data_i]['Coordinates'][name] = \
                        Result._get_data(coords_element, name, float)

                result['Data'][data_i]['Time'] = \
                    Result._get_data(data_element, 'Time', datetime)


                b_trace_data_elements = data_element.findall(\
                       ET_NS + 'BTraceData')
                b_trace_data_len = len(b_trace_data_elements)
                if b_trace_data_len > 0:

                    result['Data'][data_i]['BTraceData'] = \
                        np.empty(b_trace_data_len, dtype=object)

                    for b_trace_data_i, b_trace_data in \
                        enumerate(b_trace_data_elements):

                        result['Data'][data_i]['BTraceData'][b_trace_data_i] = {
                            'CoordinateSystem': CoordinateSystem(\
                                b_trace_data.find(\
                                    ET_NS + 'CoordinateSystem').text),
                            'Hemisphere': Hemisphere(b_trace_data.find(\
                                 ET_NS + 'Hemisphere').text),
                        }
                        for name in ['Latitude', 'Longitude', 'ArcLength']:
                            result['Data'][data_i]['BTraceData'][b_trace_data_i][name] = \
                                Result._get_data(b_trace_data, name, float)


                    for name in ['RadialLength', 'MagneticStrength',
                                 'NeutralSheetDistance', 'BowShockDistance',
                                 'MagnetoPauseDistance', 'DipoleLValue',
                                 'DipoleInvariantLatitude']:
                        result['Data'][data_i][name] = \
                            Result._get_data(data_element, name, float)


                    result['Data'][data_i]['SpacecraftRegion'] = \
                        Result._get_data(data_element, 'SpacecraftRegion',
                                         SpaceRegion)

                    for name in ['BGseX', 'BGseY', 'BGseZ']:
                        result['Data'][data_i][name] = \
                            Result._get_data(data_element, name, float)

                    for name in ['RadialTracedFootpointRegions',
                                 'NorthBTracedFootpointRegions',
                                 'SouthBTracedFootpointRegions']:
                        result['Data'][data_i][name] = \
                            Result._get_data(data_element, name,
                                             FootpointRegion)

        return result


    @staticmethod
    def _get_data(
            data_element: ET,
            name: str,
            value_type: Callable[[str], Any],
        ) -> np.ndarray:
        """
        Produces an np.ndarray(m, dtype=value_type) representation of the
        values of specified element in the given data_element ET.

        Parameters
        ----------
        data_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        name
            Name of element in data_element to get values of.
        value_type
            Type of values to get.

        Returns
        -------
        np.ndarray
            np.ndarray representation of the specified values from
            data_element.
        """
        data_elements = data_element.findall(ET_NS + name)
        size = len(data_elements)
        if size > 0:
            values = np.empty(size, dtype=value_type)
            for index, value in enumerate(data_elements):
                if value_type is datetime:
                    values[index] = dateutil.parser.parse(value.text)
                else:
                    values[index] = value_type(value.text)
        else:
            values = None

        return values


    @staticmethod
    def get_file_result(
            file_result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a FileResult from the given
        xml representation of a FileResult.

        Parameters
        ----------
        file_result_element
            ElementTree representation of a FileResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree FileResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            FileResult.
        """

        result = Result.get_status(file_result_element)
        result['Files'] = []

        for file_description in file_result_element.findall(\
                ET_NS + 'Files'):
            result['Files'].append({
                'Name': file_description.find(ET_NS + 'Name').text,
                'MimeType': file_description.find(ET_NS + 'MimeType').text,
                'Length': int(file_description.find(ET_NS + 'Length').text),
                'LastModified': dateutil.parser.parse(\
                    file_description.find(ET_NS + 'LastModified').text)
            })
        return result


#
# If I continue to return Dict instead of class objects, then the rest of
# this file can be deleted.
#
class FileDescription:
    """
    Class representing a FileDescription from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    name
        Name of file (usually a URL).
    mime_type
        MIME type of file.
    length
        Length of file in bytes.
    last_modified
        Time when file was last modified.
    """
    def __init__(
            self,
            name: str,
            mime_type: str,
            length: int,
            last_modified: datetime):
        """
        Creates a FileDescription object.

        Parameters
        ----------
        name
            Name of file (usually a URL).
        mime_type
            MIME type of file.
        length
            Length of file in bytes.
        last_modified
            Time when file was last modified.
        """
        self._name = name
        self._mime_type = mime_type
        self._length = length
        self._last_modified = last_modified

    @property
    def name(self):
        """
        Gets the name value.

        Returns
        -------
        str
            name value.
        """
        return self._name


    @name.setter
    def name(self, value):
        """
        Sets the name value.

        Parameters
        ----------
        value
            name value.
        """
        self._name = value


    @property
    def mime_type(self):
        """
        Gets the mime_type value.

        Returns
        -------
        str
            mime_type value.
        """
        return self._mime_type


    @mime_type.setter
    def mime_type(self, value):
        """
        Sets the mime_type value.

        Parameters
        ----------
        value
            mime_type value.
        """
        self._mime_type = value


    @property
    def length(self):
        """
        Gets the length value.

        Returns
        -------
        str
            length value.
        """
        return self._length


    @length.setter
    def length(self, value):
        """
        Sets the length value.

        Parameters
        ----------
        value
            length value.
        """
        self._length = value


    @property
    def last_modified(self):
        """
        Gets the last_modified value.

        Returns
        -------
        str
            last_modified value.
        """
        return self._last_modified


    @last_modified.setter
    def last_modified(self, value):
        """
        Sets the last_modified value.

        Parameters
        ----------
        value
            last_modified value.
        """
        self._last_modified = value


class FileResult(Result):
    """
    Class representing a FileResult from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Properties
    ----------
    files
        References to the files containing the requested data.
    """
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str],
            files: List[FileDescription]):
        """
        Creates an object representing a FileResult from
        <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Parameters
        ----------
        status_code
            Result status code value.
        status_sub_code
            Result status subcode value.
        status_text
            Status text.
        files
            List of files.
        """
        super().__init__(status_code, status_sub_code, status_text)
        self._files = files


    @property
    def files(self):
        """
        Gets the files value.

        Returns
        -------
        str
            files value.
        """
        return self._files


    @files.setter
    def files(self, value):
        """
        Sets the files value.

        Parameters
        ----------
        value
            files value.
        """
        self._files = value

#class CoordinateData:
#class BTraceData:
#class SatelliteData:
#class DataResult(Result):
#
