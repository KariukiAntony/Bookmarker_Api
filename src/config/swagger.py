template = {"swagger": "2.0",
            "info": {"title": "Bookmarks API",
                     "description": "API for bookmarks",
                     "contact":{"responsibleOrganization":"",
                                "responsibleDeveloper":"",
                                "email":"antonygichoya9@gmail.com",
                                "url":"www.google.com"},
                    "termsOfService": "www.google.com",
                    "version": "1.0"
                     
                     },


            "basePath": "/api/v1",
            "schemes": ["http", "https"],
            "securityDefinitions": {"Bearer": {"type": "apiKey",
                                               "name":"Authorization",
                                               "in": "header",
                                               "description": "JWT Authorization header using"+
                                               "the Bearer scheme.Example \"Authorization: Beare r{token}\""}}}
 

swagger_config = {"headers": [],
                  "specs": [{"endpoint": "apispec",
                             "route": "/apispec.json",
                             "rule_filter": lambda rule: True,
                             "model_filter": lambda tag: True,}],
                  "static_url_path": "/flasgger_static",
                  "swagger_ui":True,
                  "specs_route": "/"}