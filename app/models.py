from datetime import datetime,timezone
from app import db

class URL(db.Model):
    #Первинний ключ
    # id INTEGER PRIMARY KEY
    id = db.Column(
        db.Integer,
        primary_key = True
    )

    #вихідне посилання
    original_url = db.Column(
        db.String(2048),
        nullable = False
    )

    #Короткий код
    short_code = db.Column(
        db.String(10),
        unique = True,
        nullable = False,
        index = True
    )

    #кількість переходів
    clicks = db.Column(
        db.Integer,
        default = 0,
        nullable = False
    )

    #Час створення посилання
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable = False
    )

    def __repr__(self):
        return(
            f"<URL {self.short_code} -> "
            f"{self.original_url}>"
        )
