# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to port 5000 if not set
    app.run(debug=True, host="0.0.0.0", port=port, threaded=True)