import six
from kitty.data.report import Report

from apifuzzer.utils import try_b64encode


class ApifuzzerReport(Report):

    def __init__(self, name):
        super().__init__(name)

    def is_failed(self):
        """
        .. deprecated:: 0.6.7
            use :func:`~kitty.data.report.Report.get_status`
        """
        raise NotImplementedError('API was changed, use get_status instead')

    def to_dict(self, encoding='base64'):
        """
        Return a dictionary version of the report

        :param encoding: required encoding for the string values (default: 'base64')
        :rtype: dictionary
        :return: dictionary representation of the report
        """
        res = {}
        for k, v in self._data_fields.items():
            if isinstance(v, (bytes, bytearray, six.string_types)):
                v = try_b64encode(v)
            res[k] = v
        for k, v in self._sub_reports.items():
            res[k] = v.to_dict(encoding)
        return res
