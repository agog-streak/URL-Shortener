import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    #клас з налаштуваннями застосунку

    #ключ Flask
    SECRET_KEY=os.getenv(
        "SECRET_KEY",
        "dev-secret-key"

    )

    #URL бази даних
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///urls.db"
    )

    
    # Відключаємо відстеження змін об'єктів SQLAlchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
