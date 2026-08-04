from django.contrib.auth.decorators import user_passes_test

def provider_required(view_func):
    return user_passes_test(
        lambda user:user.is_authenticated and user.role=="PROVIDER"
    )(view_func)