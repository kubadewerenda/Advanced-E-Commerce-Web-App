from django.utils.text import slugify

def unique_slugify(instance, base_value: str, *, field: str = 'slug', queryset=None) -> str:
    base = slugify(base_value)
    slug = base
    Model = instance.__class__
    qs = queryset or Model.objects.all()
    i = 1
    while qs.filter(**{field: slug}).exists():
        slug = f'{base}-{i}'
        i += 1
    return slug
