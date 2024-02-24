import simplejson

def make_response_json(payload_obj, status_code=200, **kwargs):
    '''Return a JSON response by serializing `payload_obj`.

    Args:
        payload_obj (JSON serializable): Response payload object
        status_code (int): Response status code (default: 200)
        **kwargs: Additional parameters for simplejson.dumps

    Returns:
        tuple: Flask response consisting of JSON payload, status code, and content type header
    '''
    return (
        simplejson.dumps(payload_obj, **kwargs),
        status_code,
        {'Content-Type': 'application/json; charset=utf-8'}
    )