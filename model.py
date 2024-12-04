from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db import Base

class UserTable(Base):
    __tablename__ = 'user'
    __table_args__ = (
        {'schema': 'public'}
    )
    user_id = Column(String(50), primary_key=True, nullable=False)
    password = Column(String(50))
    username = Column(String(50))
    review_count = Column(Integer)
    total_rating = Column(Integer)
    average_rating = Column(Integer)
    reviews = relationship("ReviewTable", back_populates="user")

class StoreTable(Base):
    __tablename__ = 'store'
    __table_args__ = (
        {'schema': 'public'}
    )
    store_id = Column(Integer, primary_key=True, nullable=False)
    store_name = Column(String(50))
    store_img = Column(String)
    total_rating = Column(Integer)
    rating_count = Column(Integer)
    average_rating = Column(Integer)
    reviews = relationship("ReviewTable", back_populates="store")

class MenuTable(Base):
    __tablename__ = 'menu'
    __table_args__ = (
        {'schema': 'public'}
    )
    menu_id = Column(Integer, primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey('public.store.store_id'), nullable=False)
    menu_name = Column(String(50))
    menu_img = Column(String(50))
    description = Column(String)
    price = Column(Integer)
    is_main = Column(Boolean)

class OrderTable(Base):
    __tablename__ = 'order'
    __table_args__ = (
        {'schema': 'public'}
    )
    order_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(50), ForeignKey('public.user.user_id'), nullable=False)
    store_id = Column(Integer, ForeignKey('public.store.store_id'), nullable=False)
    menu_id = Column(Integer, ForeignKey('public.menu.menu_id'), nullable=False)
    quantity = Column(Integer)
    is_completed = Column(Boolean)
    order_date = Column(Integer)

class ReviewTable(Base):
    __tablename__ = 'review'
    __table_args__ = (
        {'schema': 'public'}
    )
    review_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(50), ForeignKey('public.user.user_id'), nullable=False)
    menu_id = Column(Integer, ForeignKey('public.menu.menu_id'), nullable=True)
    store_id = Column(Integer, ForeignKey('public.store.store_id'), nullable=False)
    rating = Column(Integer)
    content = Column(String)
    photo_url = Column(String)
    created_at = Column(Integer)
    user = relationship("UserTable", back_populates="reviews")
    store = relationship("StoreTable", back_populates="reviews")