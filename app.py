import os
from datetime import datetime
from flask import Flask, request
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# Параметры для подключения для чуда чуть ниже
DB_USER = os.getenv("POSTGRES_USER", "app")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "veryhardpassword")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "visits_db")

# Вуаля, строка для подключения не "захардкожена"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy-штуки
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Модель как в методичке
class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(50), nullable=False)

# При старте приложения создаём таблицу
with app.app_context():
    Base.metadata.create_all(bind=engine)

# Суть нашего приложения (маршрут GET /hello)
@app.route("/hello", methods=["GET"])
def hello():
    # Это тайная часть кода, про которую клиентам лучше не знать
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if client_ip and "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()

    # Берём всех зашедших на карандаш
    session = SessionLocal()
    try:
        new_visit = Visit(
            created_at=datetime.utcnow(),
            ip_address=client_ip or "unknown"
        )
        session.add(new_visit)
        session.commit()
    finally:
        session.close()

    # Записав всё что хотели, лицемерно приветливо здороваемся
    return "Hello", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)