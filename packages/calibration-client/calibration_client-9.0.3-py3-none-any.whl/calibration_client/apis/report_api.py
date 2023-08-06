"""ReportApi module class"""

import json

from ..common.base import Base


class ReportApi(Base):
    def create_report_api(self, report):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(report))

    def delete_report_api(self, report_id):
        api_url = self.__get_api_url(report_id)
        return self.api_delete(api_url)

    def update_report_api(self, report_id, report):
        api_url = self.__get_api_url(report_id)
        return self.api_put(api_url, data=json.dumps(report))

    def get_report_by_id_api(self, parameter_id):
        api_url = self.__get_api_url(parameter_id)
        return self.api_get(api_url, params={})

    def get_all_reports_by_name_api(self, name):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def get_all_reports_by_name_and_file_path_api(self, name, file_path):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'file_path': file_path})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'reports/'
        return self.get_api_url(model_name, api_specifics)
