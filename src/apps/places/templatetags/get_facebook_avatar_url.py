from django import template
from allauth.socialaccount.models import SocialAccount, SocialToken

register = template.Library()


@register.simple_tag(takes_context=True, name='get_facebook_avatar_url')
def generate_facebook_avatar_url(context):
    user = context['user']
    socialaccount = SocialAccount.objects.filter(user_id=user.id, provider='facebook').first()
    token = SocialToken.objects.get(account_id=socialaccount.id)
    access_token = token.token
    url = "https://graph.facebook.com/{}/picture?width=50&height=50&return_ssl_resources=1&access_token={}".format(
                                                                            socialaccount.uid,
                                                                            access_token
                                                                            )

    return url
