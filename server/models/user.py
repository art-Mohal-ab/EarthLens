from sqlalchemy import Column, Integer, String
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    def set_password(self, password: str):
        password = password[:72]
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        password = password[:72]
        return check_password_hash(self.password_hash, password)
