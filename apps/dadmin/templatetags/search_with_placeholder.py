from django.contrib.admin.templatetags.admin_list import (register, search_form)
from django.contrib.admin.templatetags.base import InclusionAdminNode


def search_form_plus(cl, search_placeholder: str = ""):
    """
    Display a search form for searching the list with placeholder.
    """
    return dict(search_form(cl), search_placeholder=search_placeholder)


@register.tag(name='search_form_plus')
def search_form_tag(parser, token):
    return InclusionAdminNode(parser, token, func=search_form_plus, template_name='search_form_plus.html', takes_context=False)