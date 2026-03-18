from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from datetime import datetime
import uvicorn

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./crypto_portfolio.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class PortfolioEntry(Base):
    __tablename__ = "portfolio_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crypto = Column(String)
    amount = Column(Float)
    purchase_price = Column(Float)
    user = relationship("User")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crypto = Column(String)
    amount = Column(Float)
    transaction_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class CryptoPrice(Base):
    __tablename__ = "crypto_prices"
    crypto = Column(String, primary_key=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data():
    db = SessionLocal()
    if not db.query(User).first():
        user = User(username="demo", email="demo@example.com", password_hash=get_password_hash("password"))
        db.add(user)
        db.commit()
        db.refresh(user)

        portfolio_entry = PortfolioEntry(user_id=user.id, crypto="BTC", amount=1.5, purchase_price=45000.0)
        db.add(portfolio_entry)

        transaction = Transaction(user_id=user.id, crypto="BTC", amount=1.5, transaction_type="buy")
        db.add(transaction)

        crypto_price = CryptoPrice(crypto="BTC", price=47000.0)
        db.add(crypto_price)

        db.commit()
    db.close()

seed_data()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard():
    with open("templates/dashboard.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/portfolio", response_class=HTMLResponse)
async def read_portfolio():
    with open("templates/portfolio.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/transactions", response_class=HTMLResponse)
async def read_transactions():
    with open("templates/transactions.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/analytics", response_class=HTMLResponse)
async def read_analytics():
    with open("templates/analytics.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/profile", response_class=HTMLResponse)
async def read_profile():
    with open("templates/profile.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/portfolios")
async def get_portfolios(db: SessionLocal = Depends(get_db)):
    portfolios = db.query(PortfolioEntry).all()
    return portfolios

@app.post("/api/portfolios")
async def add_portfolio(crypto: str, amount: float, purchase_price: float, db: SessionLocal = Depends(get_db)):
    portfolio_entry = PortfolioEntry(crypto=crypto, amount=amount, purchase_price=purchase_price)
    db.add(portfolio_entry)
    db.commit()
    db.refresh(portfolio_entry)
    return portfolio_entry

@app.get("/api/transactions")
async def get_transactions(db: SessionLocal = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

@app.post("/api/transactions")
async def add_transaction(crypto: str, amount: float, transaction_type: str, db: SessionLocal = Depends(get_db)):
    transaction = Transaction(crypto=crypto, amount=amount, transaction_type=transaction_type)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@app.get("/api/user")
async def get_user(db: SessionLocal = Depends(get_db)):
    user = db.query(User).first()
    return user

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
