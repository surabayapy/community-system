from api_v1 import app

app.config.from_object('config.DevelopmentConfig')

app.run()