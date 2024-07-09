import datetime as dt
import json
import os

from pyzoom import ZoomClient
from lingoclub.settings import ZOOM_CLIENT_ID, ZOOM_AUTH_TOKEN


class ZoomAuth:
    def __init__(self):
        pass

    # def get_server_to_server_token(self):
    #     self.client.add_header('Host', 'zoom.us')
    #     self.client.add_header('Authorization', f'Basic {self.token}')
    #     payload = {'grant_type': 'account_credentials',
    #                'account_id': self.accountId}
    #     self.client.payload = payload
    #     resp = self.client.retrieve_post_response()
    #     print(resp.content)

    def _get_token(self):
        resp = os.popen(f"curl -X POST https://zoom.us/oauth/token -d 'grant_type=account_credentials' -d 'account_id={ZOOM_CLIENT_ID}' -H 'Host: zoom.us' -H 'Authorization: Basic {ZOOM_AUTH_TOKEN}'").read()
        content = json.loads(resp)
        return content

    def get_meeting_url(self):
        t = self._get_token()
        client = ZoomClient(t['access_token'])

        # Creating a meeting
        meeting = client.meetings.create_meeting('Auto created 1', start_time=dt.datetime(2024, 1, 11, 10).isoformat(), duration_min=60,
                                                 password='not-secure')
        return meeting['join_url']

        # Update a meeting
        # meeting = client.meetings.update_meeting('Auto updated 1', meeting_id = meeting.id ,start_time=dt.now().isoformat(), duration_min=60,password='not-secure')

        # Adding registrants
        # client.meetings.add_meeting_registrant(meeting.id, first_name='John', last_name='Doe', email='john.doe@example.com')


if __name__ == '__main__':
    # get_access_token()
    # meetings()
    c = ZoomAuth()
    # c.get_server_to_server_token()
    c.get_meeting_url()
