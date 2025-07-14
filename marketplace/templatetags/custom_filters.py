from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    print(dictionary, key, "************************")
    print(dictionary, key, "&&&&&&&&&")
    key = int(key) if isinstance(key, str) and key.isdigit() else key
    return dictionary.get(key, 0)