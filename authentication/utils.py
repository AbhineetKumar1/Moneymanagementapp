from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six 

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.is_active) + six.text_type(user.pk) + six.text_type(timestamp)
            # Replace the above line with the following:
            # f"{user.is_active}{user.pk}{timestamp}"
        )

account_activation_token = AppTokenGenerator()