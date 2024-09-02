def lambda_handler(event, context):
    # Extract the CloudFront request from the event
    request = event['Records'][0]['cf']['request']
    uri = request['uri']
    
    # Logic to set the custom header based on the original URI path
    if uri == '/':
        header_value = 'server01'
    elif '/server02' in uri:
        header_value = 'server02'
    elif '/server03' in uri:
        header_value = 'server03'
    else:
        header_value = 'default'  # Fallback header value if the path doesn't match
    
    # Set the custom header based on the URI path
    request['headers']['x-custom-header'] = [{
        'key': 'X-Custom-Header',
        'value': header_value
    }]
    
    # Statically reset the URI to a valid path
    request['uri'] = '/'  # This sets the URI to the root path
    
    # Return the modified request
    return request