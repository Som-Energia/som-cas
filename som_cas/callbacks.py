def participa(user, service):
    """
    Attributes for participa.somenergia.coop service
    """
    attributes = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'soci': user.www_soci,
        'locale': user.lang
    }

    return attributes

def formacio(user, service):
    """
    Attributes for formacio.somenergia.coop service
    """
    attributes = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'soci': user.www_soci,
        'locale': user.lang
    }

    return attributes
