
def validate_field(**kwargs):
    for key, value in kwargs.items():
        if value is None:
            return key
        if value.strip() == '':
            return key
        if len(value) < 1:
            return key
        if value.startswith(';', 2):
            return key
