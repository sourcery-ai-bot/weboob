# -*- coding: utf-8 -*-

# Copyright(C) 2013      Vincent A
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


from weboob.deprecated.browser import Browser
from weboob.tools.date import datetime
from weboob.deprecated.browser.parsers.jsonparser import json
from urllib import urlencode

#from .pages import Page1, Page2


__all__ = ['GuerrillamailBrowser']


class GuerrillamailBrowser(Browser):
    PROTOCOL = 'https'
    DOMAIN = 'www.guerrillamail.com'
    ENCODING = 'utf-8'

    def __init__(self, *args, **kw):
        kw['parser'] = 'raw'
        Browser.__init__(self, *args, **kw)

    def _get_unicode(self, url, *a):
        return self.get_document(self.openurl(url, *a)).decode(self.ENCODING, 'replace')

    def _get_json(self, url, *a):
        return json.loads(self._get_unicode(url, *a))

    def get_mails(self, boxid):
        params = {'email_user': boxid, 'lang': 'en', 'domain': 'guerrillamail.com'}
        d = self._get_json('https://www.guerrillamail.com/ajax.php?f=set_email_user', urlencode(params))

        d = self._get_json('https://www.guerrillamail.com/ajax.php?f=get_email_list&offset=0&domain=guerrillamail.com')
        for m in d['list']:
            info = {}
            info['id'] = m['mail_id']
            info['from'] = m['mail_from']
#            info['to'] = m['mail_recipient']
            info['to'] = '%s@guerrillamail.com' % boxid
            info['subject'] = m['mail_subject']
            info['datetime'] = datetime.fromtimestamp(int(m['mail_timestamp']))
            info['read'] = bool(int(m['mail_read']))
            yield info

    def get_mail_content(self, mailid):
        d = self._get_json('https://www.guerrillamail.com/ajax.php?f=fetch_email&email_id=mr_%s&domain=guerrillamail.com' % mailid)
        return d['mail_body']

    def send_mail(self, from_, to, subject, body):
        params = {'from': from_, 'to': to, 'subject': subject, 'body': body, 'attach': '', 'domain': 'guerrillamail.com'}
        self._get_json('https://www.guerrillamail.com/ajax.php?f=send_email', urlencode(params))
