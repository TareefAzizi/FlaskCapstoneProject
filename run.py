from application import app
import os


if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))