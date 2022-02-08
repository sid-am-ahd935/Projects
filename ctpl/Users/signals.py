def populate_models(sender, **kwargs):
    from django.contrib.auth.models import User
    from django.contrib.auth.models import group
    # create groups
    # assign permissions to groups
    # create users