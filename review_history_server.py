from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from model import ReviewTable, UserTable, StoreTable
from db import session
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta
import os
import uvicorn

review_history = FastAPI()

review_history.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

review_history.add_middleware(SessionMiddleware, secret_key="your-secret-key")

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

#로그인 상태 확인, 로그인 중인 유저 아이디 반환
@review_history.get("/check_login/")
async def check_login(request: Request):
    # 세션에서 사용자 정보 확인
    if "user_id" not in request.session:
        return False
    
    return {"user_id": f"{request.session['user_id']}"}

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

#유저가 작성한 가장 최근 리뷰의 월부터 6개월과 각 달의 팽균 별점 리스트 딕셔너리 반환
@review_history.get("/chart_data/{user_id}")
async def read_chart_data(user_id: str, db: Session = Depends(get_db)):
    six_months_ago = datetime.now() - timedelta(days=180)
    
    reviews = db.query(ReviewTable.created_at, ReviewTable.rating) \
        .filter(ReviewTable.user_id == user_id, ReviewTable.created_at >= six_months_ago) \
        .all()
    
    data = {
        "months": [],
        "ratings": []
    }
    
    for review in reviews:
        month = review.created_at.strftime('%m') + "월"
        rating = review.rating
        
        if month not in data["months"]:
            data["months"].append(month)
            data["ratings"].append([rating])
        else:
            index = data["months"].index(month)
            data["ratings"][index].append(rating)
    
    for i in range(len(data["ratings"])):
        avg_rating = sum(data["ratings"][i]) / len(data["ratings"][i])
        data["ratings"][i] = "{:.1f}".format(avg_rating)

    return data
    
if __name__ == "__review_history__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)