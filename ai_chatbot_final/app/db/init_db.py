from app.db.database import engine, Base
from app.models.chat_log import ChatLog

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized")
