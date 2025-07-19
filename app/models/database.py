import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import urllib.parse
import uuid

try:
    from pgvector.sqlalchemy import Vector
    VECTOR_AVAILABLE = True
except ImportError:
    # Fallback to TEXT if pgvector is not available
    from sqlalchemy import Text as Vector
    VECTOR_AVAILABLE = False

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column('user_id', Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column('password_hash', String(255), nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    documents = relationship("Document", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column('document_id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    document_name = Column(String(255), nullable=False)
    document_type = Column(String(50))
    file_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = 'chunks'
    
    id = Column('chunk_id', Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.document_id'))
    chunk_text = Column(Text, nullable=False)
    chunk_order = Column(Integer)
    
    document = relationship("Document", back_populates="chunks")
    embedding = relationship("Embedding", back_populates="chunk", uselist=False, cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="related_chunk")

class Embedding(Base):
    __tablename__ = 'embeddings'
    
    id = Column('embedding_id', Integer, primary_key=True)
    chunk_id = Column(Integer, ForeignKey('chunks.chunk_id'), unique=True)
    embedding_vector = Column(Vector(768) if VECTOR_AVAILABLE else Text)  # 768 for text-embedding-004 model
    
    chunk = relationship("Chunk", back_populates="embedding")

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column('conversation_id', String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    session_type = Column(String(100), nullable=True)  # Store analysis type
    started_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column('message_id', Integer, primary_key=True)
    conversation_id = Column(String(36), ForeignKey('conversations.conversation_id'))
    sender = Column(String(10), nullable=False)
    message_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    related_chunk_id = Column(Integer, ForeignKey('chunks.chunk_id'), nullable=True)
    
    conversation = relationship("Conversation", back_populates="messages")
    related_chunk = relationship("Chunk", back_populates="messages")

def init_db(connection_string=None):
    try:
        if connection_string is None:
            # Try to get DATABASE_URL from environment first (for deployment)
            connection_string = os.environ.get('DATABASE_URL')
            
            if not connection_string:
                # Fallback to individual environment variables
                username = os.environ.get('DB_USER', 'postgres')
                password = urllib.parse.quote_plus(os.environ.get('DB_PASS', '123456@rR'))
                host = os.environ.get('DB_HOST', 'db.dsrysmorxbcuftrwulpa.supabase.co')
                port = os.environ.get('DB_PORT', '5432')
                database = os.environ.get('DB_NAME', 'postgres')
                
                connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
        
        # Create engine with connection pooling and retry logic
        engine = create_engine(
            connection_string,
            pool_size=10,                    # Number of connections to maintain
            max_overflow=20,                 # Additional connections allowed
            pool_pre_ping=True,              # Validate connections before use
            pool_recycle=3600,               # Recycle connections after 1 hour
            connect_args={
                "connect_timeout": 30,       # Connection timeout in seconds
                "application_name": "police_case_analysis",
                "options": "-c statement_timeout=30000"  # Query timeout in milliseconds
            }
        )
        
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        
        print("Database initialized successfully with PostgreSQL and connection pooling")
        return Session
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
