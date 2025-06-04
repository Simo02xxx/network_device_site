from app import create_app
from flask_wtf import CSRFProtect

app = create_app()
csrf = CSRFProtect(app)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)