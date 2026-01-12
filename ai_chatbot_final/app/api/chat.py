# # from fastapi import APIRouter, Depends
# # from sqlalchemy.orm import Session
# # from app.core.security import verify_api_key
# # from app.db.database import SessionLocal
# # from app.services.langchain_service import ask_llm
# # from app.models.chat_log import ChatLog
# #
# # router = APIRouter()
# #
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()
# #
# # @router.get("/chat")
# # def chat(
# #     q: str,
# #     db: Session = Depends(get_db),
# #     _: str = Depends(verify_api_key)
# # ):
# #     answer = ask_llm(q)
# #
# #     log = ChatLog(question=q, answer=answer)
# #     db.add(log)
# #     db.commit()
# #
# #     return {"question": q, "answer": answer}
#
#
# from fastapi import APIRouter, Depends, HTTPException, Header
# from sqlalchemy.orm import Session
# from app.db.database import SessionLocal
# from app.models import ChatLog
# from app.services.langchain_service import ask_llm
# from app.core.config import API_KEY
#
# router = APIRouter()
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @router.get("/chat")
# def chat(
#     q: str,
#     x_api_key: str = Header(...),
#     db: Session = Depends(get_db)
# ):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API Key")
#
#     answer = ask_llm(q)
#
#     chat_log = ChatLog(
#         question=q,
#         answer=answer
#     )
#
#     db.add(chat_log)
#     db.commit()
#     db.refresh(chat_log)
#
#     return {
#         "question": q,
#         "answer": answer
#     }
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.chat_log import ChatLog
from app.core.security import verify_api_key
# from app.services.llm import get_answer
# from app.services.langchain_service import llm
from app.services.langchain_service import ask_llm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/chat")
def chat(
    q: str,
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    verify_api_key(x_api_key)

    # 1️⃣ get LLM answer FIRST
    answer = ask_llm(q)

    # 2️⃣ save to DB
    chat_log = ChatLog(
        question=q,
        answer=answer
    )

    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)

    return {
        "question": q,
        "answer": answer
    }
