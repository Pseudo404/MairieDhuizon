"""(Super Admin vs Admin 'simple')"""

def get_admin_account(user):
    """ Admin account connecté ou pas """
    if not user.is_authenticated:
        return None
    if hasattr(user, 'admin_account'):
        return user.admin_account
    return None


def user_is_super_admin(user):
    """ Super admin or just admin """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    account = get_admin_account(user)
    return account is not None and account.is_super_admin


def user_is_panel_admin(user):
    """ Acces au panel admin """
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return get_admin_account(user) is not None
