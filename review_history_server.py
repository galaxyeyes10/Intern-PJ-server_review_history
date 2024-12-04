from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from model import ReviewTable, UserTable, StoreTable
from db import session
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

review_history = FastAPI()

review_history.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

#닉네임 반환
@review_history.get("/username/{user_id}")
async def read_username(user_id: str, db: Session = Depends(get_db)):
    reviewer = db.query(ReviewTable).join(UserTable).filter(ReviewTable.user_id == user_id).first()
    
    return reviewer.user.username

#동일 유저의 리뷰 갯수 키운트
@review_history.get("/review_counting/{user_id}")
async def read_review_count(user_id: str, db: Session = Depends(get_db)):
    reviews = db.query(ReviewTable).filter(ReviewTable.user_id == user_id).all()
    return len(reviews)

#동일 유저의 평균 별점 계산
@review_history.get("/average_rating/{user_id}")
async def average_rating(user_id: str, db: Session = Depends(get_db)):
    reviews = db.query(ReviewTable).filter(ReviewTable.user_id == user_id).all()
    ratings = [row.rating for row in reviews]
    average = sum(ratings) / len(ratings)
    return round(average, 1)

#리뷰 내역 딕셔너리 반환
@review_history.get("/review_history/{user_id}")
async def read_review_history(user_id: str, db: Session = Depends(get_db)):
    reviews = db.query(ReviewTable.created_at,
                        StoreTable.store_name,
                        ReviewTable.rating).join(StoreTable, ReviewTable.store_id == StoreTable.store_id).filter(ReviewTable.user_id == user_id).all()
    
    history = [
        {
            "date": str(review.created_at)[0:11],
            "storeName": review.store_name,
            "rating": "{:.1f}".format(review.rating)
        }
        for review in reviews
    ]

    return history

if __name__ == "__review_history__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)