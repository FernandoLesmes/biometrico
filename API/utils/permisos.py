from API.models import PermisoRol

def tiene_permiso(user, vista):
    if not hasattr(user, 'hremployee'):
        return False
    
    rol_id = user.hremployee.emp_role.id
    try:
        permiso = PermisoRol.objects.get(rol_id=rol_id, vista=vista)
        return permiso.tiene_acceso
    except PermisoRol.DoesNotExist:
        return False
