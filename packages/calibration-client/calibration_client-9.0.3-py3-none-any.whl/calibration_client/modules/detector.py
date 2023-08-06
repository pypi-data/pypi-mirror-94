"""Detector module class"""

from http import HTTPStatus

from ..common.base import Base
from ..common.config import DETECTOR, CREATE, DELETE, UPDATE, GET

MODULE_NAME = DETECTOR


class Detector:
    def __init__(self, calibration_client,
                 name, identifier, karabo_name, karabo_id_control,
                 flg_available, description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.name = name
        self.identifier = identifier
        self.karabo_name = karabo_name
        self.karabo_id_control = karabo_id_control
        self.flg_available = flg_available
        self.description = description

    def create(self):
        cal_client = self.calibration_client
        response = cal_client.create_detector_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(
            response, CREATE, HTTPStatus.CREATED, MODULE_NAME
        )

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        cal_client = self.calibration_client
        response = cal_client.delete_detector_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(
            response, DELETE, HTTPStatus.NO_CONTENT, MODULE_NAME
        )

    def update(self):
        cal_client = self.calibration_client
        response = cal_client.update_detector_api(self.id,
                                                  self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(
            response, UPDATE, HTTPStatus.OK, MODULE_NAME
        )

    @staticmethod
    def get_by_id(cal_client, detector_id):
        response = cal_client.get_detector_by_id_api(detector_id)

        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(cal_client, name):
        response = cal_client.get_all_detectors_by_name_api(name)

        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_identifier(cal_client, identifier):
        response = cal_client.get_all_detectors_by_identifier_api(identifier)

        Base.cal_debug(MODULE_NAME, 'get_all_by_identifier', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_by_name(cal_client, name):
        res = Detector.get_all_by_name(cal_client, name)

        if res['success']:
            if res['data'] == []:
                resp_data = []
            else:
                resp_data = res['data'][0]

            res = {'success': res['success'],
                   'info': res['info'],
                   'app_info': res['app_info'],
                   'data': resp_data}

        return res

    @staticmethod
    def get_by_identifier(cal_client, identifier):
        res = Detector.get_all_by_identifier(cal_client, identifier)

        if res['success']:
            if res['data'] == []:
                resp_data = []
            else:
                resp_data = res['data'][0]

            res = {'success': res['success'],
                   'info': res['info'],
                   'app_info': res['app_info'],
                   'data': resp_data}

        return res

    def __get_resource(self):
        detector = {
            DETECTOR: {
                'name': self.name,
                'identifier': self.identifier,
                'karabo_name': self.karabo_name,
                'karabo_id_control': self.karabo_id_control,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return detector
