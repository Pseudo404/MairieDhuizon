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

def user_is_only_centre_loisirs_admin(user):
    """ Vrai si l'utilisateur est uniquement admin centre de loisirs (pas super admin) """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return False
    account = get_admin_account(user)
    return account is not None and account.is_centre_loisirs and not account.is_super_admin

def user_is_panel_admin(user):
    """ Acces au panel admin """
    if not user.is_authenticated:
        return False
    if user_is_only_centre_loisirs_admin(user):
        return False
    if user.is_staff:
        return True
    return get_admin_account(user) is not None

def user_is_centre_loisirs_admin(user):
    """
    Acces au panel centre de loisirs.
    Ont accès :
      - Les superusers Django
      - Les super admins (is_super_admin)
      - Les comptes avec is_centre_loisirs (accès CL uniquement)
      - Les admins classiques avec can_access_centre_loisirs (panel + CL)
    N'ont PAS accès :
      - Les utilisateurs non authentifiés
    """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    account = get_admin_account(user)
    if account is None:
        return False
    return (
        account.is_super_admin
        or account.is_centre_loisirs
        or account.can_access_centre_loisirs
    )
