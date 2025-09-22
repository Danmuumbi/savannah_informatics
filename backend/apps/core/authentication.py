from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.openid_connect.views import OpenIDConnectAdapter
from allauth.socialaccount.providers.openid_connect.client import OIDCClient
from allauth.socialaccount.providers.oauth2.client import OAuth2Error

class CustomOpenIDConnectAdapter(OpenIDConnectAdapter):
    def complete_login(self, request, app, token, response):
        try:
            client = OIDCClient(
                self.get_provider(),
                app,
                token.token,
                response.get('id_token', '')
            )
            userinfo = client.userinfo()
            return self.get_provider().sociallogin_from_response(request, userinfo)
        except OAuth2Error as e:
            raise e