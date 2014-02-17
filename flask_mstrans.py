import datetime
import json
import urllib
import httplib

from flask.ext.babel import gettext
from flask import current_app, g, session


try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class MsTranslate(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        self._token = ''
        self._token_time = None
        self.ms_translate_id = self.app.config.get('MS_TRANSLATE_ID')
        self.ms_translate_secret = self.app.config.get('MS_TRANSLATE_SECRET')

    def init_app(self, app):
        self.app = app
        self.get_token()
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mstrans'] = self
        app.jinja_env.filters.setdefault('translate', self.translate)

    @property
    def token(self):
        # if self._token_time: print (datetime.datetime.now() - self._token_time).seconds
        if self._token_time and (datetime.datetime.now() - self._token_time).seconds < 540:
            return self._token
        self.get_token()
        return self._token

    def get_token(self):
        try:
            # get access token
            params = urllib.urlencode({
                'client_id': self.ms_translate_id,
                'client_secret': self.ms_translate_secret,
                'scope': 'http://api.microsofttranslator.com',
                'grant_type': 'client_credentials'
            })
            conn = httplib.HTTPSConnection("datamarket.accesscontrol.windows.net")
            conn.request("POST", "/v2/OAuth2-13", params)
            response = json.loads(conn.getresponse().read())
            self._token = response[u'access_token']
            self._token_time = datetime.datetime.now()
        except Exception, e:
            return gettext('Unexpected error: %s ' % e)

    def translate(self, text, destLang='en', sourceLang=''):
        if self.ms_translate_id == "" or self.ms_translate_secret == "":
            return gettext('Error: translation service not configured.')
        try:

            # translate
            conn = httplib.HTTPConnection('api.microsofttranslator.com')
            params = {
                'appId': 'Bearer ' + self.token,
                'from': sourceLang,
                'to': destLang,
                'text': text.encode("utf-8")
            }
            conn.request("GET", '/V2/Ajax.svc/Translate?' + urllib.urlencode(params))
            response = json.loads("{\"response\":" + conn.getresponse().read().decode('utf-8-sig') + "}")
            return response["response"]
        except Exception, e:
            return gettext('Error: Unexpected error: %s ' % e)


    def translate_array(self, arr, destLang='en', sourceLang=''):
        if self.ms_translate_id == "" or self.ms_translate_secret == "":
            return gettext('Error: translation service not configured.')
        try:
            # translate
            conn = httplib.HTTPConnection('api.microsofttranslator.com')
            params = {
                'appId': 'Bearer ' + self.token,
                'from': sourceLang,
                'to': destLang,
                'texts': json.dumps([text.encode("utf-8") for text in arr])
            }
            conn.request("GET", '/V2/Ajax.svc/TranslateArray?' + urllib.urlencode(params))
            response = json.loads("{\"response\":" + conn.getresponse().read().decode('utf-8-sig') + "}")
            return response["response"]
        except:
            return gettext('Error: Unexpected error.')