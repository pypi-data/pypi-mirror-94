from sixgill.sixgill_base_client import SixgillBaseClient
from sixgill.sixgill_request_classes.sixgill_actionable_alerts_request import SixgillActionableAlertsGetRequest
from sixgill.sixgill_request_classes.sixgill_specific_actionable_alert_request import \
    SixgillSpecificActionableAlertGetRequest
from sixgill.sixgill_request_classes.sixgill_actionable_alert_content_request import \
    SixgillActionableAlertContentGetRequest


class SixgillActionableAlertClient(SixgillBaseClient):

    def __init__(self, client_id, client_secret, channel_id, logger=None, session=None, verify=False,
                 num_of_attempts=5):
        super(SixgillActionableAlertClient, self).__init__(client_id=client_id, client_secret=client_secret,
                                                           channel_id=channel_id, logger=logger,
                                                           session=session, verify=verify,
                                                           num_of_attempts=num_of_attempts)

    def get_actionable_alerts_bulk(self, limit=50, offset=0, sort_by=None,
                                   sort_order=None, is_read=None, threat_level=None,
                                   threat_type=None):
        return self._send_request(SixgillActionableAlertsGetRequest(self.channel_id, self._get_access_token(),
                                                                    limit, offset, sort_by, sort_order, is_read,
                                                                    threat_level, threat_type))

    def get_actionable_alert(self, actionable_alert_id):
        return self._send_request(SixgillSpecificActionableAlertGetRequest(self.channel_id, self._get_access_token(),
                                                                           actionable_alert_id))

    def get_actionable_alert_content(self, actionable_alert_id):
        raw_response = self._send_request(
            SixgillActionableAlertContentGetRequest(self.channel_id, self._get_access_token(),
                                                    actionable_alert_id))
        alert_content = raw_response.get('content', {"items": [], "total": 0})

        return alert_content
