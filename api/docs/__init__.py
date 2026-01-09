import azure.functions as func
import json
import os
from pathlib import Path

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Serve OpenAPI documentation (Swagger UI)
    Only available locally for security
    """

    # Só permitir em ambiente local
    is_local = os.getenv('AZURE_FUNCTIONS_ENVIRONMENT') != 'Production'

    if not is_local:
        return func.HttpResponse(
            json.dumps({'error': 'Documentation only available in local environment'}),
            status_code=403,
            mimetype='application/json'
        )

    # Ler o arquivo openapi.json
    current_dir = Path(__file__).parent
    openapi_file = current_dir / 'openapi.json'

    with open(openapi_file, 'r') as f:
        openapi_spec = f.read()

    # HTML com Swagger UI
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Battle Reports API - Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui.css" />
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {{
                const ui = SwaggerUIBundle({{
                    spec: {openapi_spec},
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                }});
                window.ui = ui;
            }};
        </script>
    </body>
    </html>
    """

    return func.HttpResponse(
        html,
        mimetype='text/html',
        status_code=200
    )