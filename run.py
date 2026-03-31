import os
from service import app

# Ambil port dari environment atau default ke 8080 sesuai instruksi lab
port = int(os.getenv("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)