from django.template import Library
from django.utils.translation import gettext as _


register = Library()


@register.filter
def assembly_event(value):
    if value.is_general_assembly:
        return _("l'Assamblea General")

    conector_text = ''
    if value.local_group.name[0].upper() in ['AEIOU']:
        conector_text = _('l\'')
    base_text = _("l'Assemblea Ordinària de la")
    return f'{base_text} {conector_text}{value.local_group.full_name}'