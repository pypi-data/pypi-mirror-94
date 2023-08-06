"""
Fields to be added to all resources
"""
COMMON_FIELDS = {
    '_tags': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    '_x': {
        'allow_unknown': True
    }
}
