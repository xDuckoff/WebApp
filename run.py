from app import app
from beaker.middleware import SessionMiddleware

app.run(debug=True)
