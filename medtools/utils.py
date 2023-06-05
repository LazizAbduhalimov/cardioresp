def get_verbose_name(model, field):
    return model._meta.get_field(field).verbose_name.title()