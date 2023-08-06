class defaults:
    httpVersion = "1.1" # DONT CHANGE THIS UNLESS YOU KNOW EXACLTY WHAT YOU ARE DOING!
    serverName = "Sonoma/1.0" # SERVER NAME/VERSION. THIS WILL SHOW IN THE RESPONSE HEADER TO VISITORS. YOU CAN CHANGE THIS TO ANYTHING.
    defaultOrigin = "*" # DEFAULT ORIGIN HEADER. THE HEADER WILL DISPLAY THIS VALUE UNLESS OTHERWISE CHANGED IN YOU CUSTOM HANDLER.
    # DEFAULT RESPONSE FOR DEFAULT HANDLER, YOU ARE ENCOURAGED TO CHANGE THIS IF YOU ARE NOT USING A CUSTOM HANDLER.
    defaultResponse = """ 
        <!DOCTYPE html><html><head>
        <style>html, body{ margin: 0 auto;text-align:center; }</style>
        </head><body>
        <h1 style=\"text-align:center;\">Hello World!</h1>
        <span>This is the default webpage for %s.</span>
        </body></html>"
        """ % serverName 