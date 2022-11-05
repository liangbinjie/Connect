from connectApp import create_app, db
import os

app = create_app()
db.create_all(app=app)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=os.environ("$POST"))
