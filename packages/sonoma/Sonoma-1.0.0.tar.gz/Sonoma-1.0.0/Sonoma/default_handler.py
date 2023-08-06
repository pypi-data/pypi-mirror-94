from http import HTTPStatus
from defaults import defaults

def defaultHandler(self, requestStatusLine, requestHeaders, requestBody, client_connection, client_address):
    """
    ## Supported Methods:
    - GET
    - HEAD
    """
    
    # SERVE GET
    if requestStatusLine.split()[0].lower() == "get":
        responseStatusLine, responseHeaders = self.httpHeaders(HTTPStatus.OK, contentType="html")
        responseBody = defaults.defaultResponse
        
        return (responseStatusLine, responseHeaders, responseBody)

    # SERVE HEAD
    elif requestStatusLine.split()[0].lower() == "head":   
        responseStatusLine, responseHeaders = self.httpHeaders(HTTPStatus.OK, contentType="text")
        return (responseStatusLine, responseHeaders, "")  
    
    # RESPOND WITH 405 STATUS - METHOD NOT ALLOWED
    else:
        responseStatusLine, responseHeaders = self.httpHeaders(HTTPStatus.METHOD_NOT_ALLOWED, contentType="text")
        return (responseStatusLine, responseHeaders, "")    