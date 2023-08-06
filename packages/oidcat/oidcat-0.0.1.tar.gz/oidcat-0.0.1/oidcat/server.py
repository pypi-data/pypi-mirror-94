import os
import json
import flask
from flask import request
import flask_oidc


import functools, base64


class OpenIDConnect(flask_oidc.OpenIDConnect):
    @functools.wraps(flask_oidc.OpenIDConnect.__init__)
    def __init__(self, app, credentials_store=None, *a, **kw):
        if isinstance(credentials_store, str):
            import sqlitedict
            credentials_store = sqlitedict.SqliteDict(
                credentials_store, autocommit=True)
        super().__init__(app, credentials_store, *a, **kw)

    def accept_token(self, scopes_required=None, keycloak_role=None, client=True,
                     require_token=True, checks=None):
        checks = checks or []

        def wrapper(view_func):
            @functools.wraps(view_func)
            def decorated(*args, **kwargs):
                # get token
                token = self.__get_access_token_from_request()
                # check if token is valid
                validity = self.validate_token(token, scopes_required) if token else 'No token'
                if validity is True:
                    token_info = self._parse_token_info(token)
                    print(token_info)
                    print(token)
                    if (not self.has_keycloak_role(keycloak_role, token_info, client=client) or
                            not all(chk(token_info) for chk in checks)):
                        validity = 'Insufficient privileges.'

                # yes it is!
                if validity is True or not require_token:
                    return view_func(*args, **kwargs)

                # No! I'm not supposed to talk to strangers!
                return flask.jsonify({
                    'error': 'invalid_token',
                    'error_description': validity
                }), 401, {'WWW-Authenticate': 'Bearer'}
            return decorated
        return wrapper

    def __get_access_token_from_request(self):
        token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(None,1)[1].strip()
        return (
            token or
            request.form.get('access_token') or
            request.args.get('access_token') or
            flask.g.oidc_id_token and self.get_access_token() or None)

    def _parse_token_info(self, token=None):
        if not isinstance(token, dict):
            header, tkn, signature = (token or self.get_access_token()).split('.')
            token = json.loads(base64.b64decode(tkn + '==='))
        return token

    def has_keycloak_role(self, roles, token=None, client=True):
        if not roles:
            return True
        token = self._parse_token_info(token)
        # get roles from token
        user_roles = token['realm_access']['roles'] if 'realm_access' in token else []
        if client:
            if client is True:
                client = self.client_secrets['client_id']
            try:
                user_roles += token['resource_access'][client]['roles']
            except KeyError:
                pass
        # compare roles
        roles = {roles} if isinstance(roles, str) else set(roles)
        return roles.issubset(set(user_roles))

    # def load_secrets(self, app):  # this is from master, but is not available in the current pip package
    #     # Load client_secrets.json to pre-initialize some configuration
    #     return _json_loads(app.config['OIDC_CLIENT_SECRETS'])

# https://github.com/googleapis/oauth2client/blob/0d1c814779c21503307b2f255dabcf24b2a107ac/oauth2client/clientsecrets.py#L119
# def _json_loads(content):
#     if isinstance(content, dict):
#         return content
#     if os.path.isfile(content):
#         with open(content, 'r') as f:
#             content = f.read()
#     if not isinstance(content, str):
#         content = content.decode('utf-8')
#     return json.loads(content)
