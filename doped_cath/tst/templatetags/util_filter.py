import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()


def getattribute_none(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        attr = getattr(value, str(arg));
        if callable(attr):
            return attr();
        else:
            return attr
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return 'None'

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
    	attr = getattr(value, str(arg));
    	if callable(attr):
	        return attr();
        else:
        	return attr
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID + ' ' + arg

def getattribute_iter(value, args):
    args = args.split('__');
    # value 
    for arg in args:
        if arg:
            value = getattribute(value,arg);
        else:
            pass

    return value

# @register.filter
def get_type(value):
    return type(value).__name__

register.filter('getattribute', getattribute)
register.filter('getattribute_iter', getattribute_iter)
register.filter('getattribute_none', getattribute_none)
register.filter('get_type', get_type)
