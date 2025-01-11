from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'  # Change the keyword to 'Bearer'


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Handle None case for last_login and date_joined
        try:
            if user.last_login is None:
                last_login = ''
            else:
                last_login = user.last_login.replace(microsecond=0, tzinfo=None)
        except AttributeError:
            last_login = ''

        date_joined = user.date_joined.replace(microsecond=0, tzinfo=None)

        return f"{user.pk}{last_login}{date_joined}{timestamp}"


# Instantiate the custom token generator
custom_token_generator = CustomPasswordResetTokenGenerator()