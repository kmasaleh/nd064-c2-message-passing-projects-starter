import os
import sys
dirname = os.path.dirname(__file__)
sys.path.append(dirname)
filename = os.path.join(dirname, '../../')
sys.path.append(filename)


from app import create_app


app = create_app(os.getenv("FLASK_ENV") or "test")

if __name__ == "__main__":
    app.run(debug=True)
