import os
from app.api.v1 import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == "__main__":
    app.run()
