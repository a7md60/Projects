from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Any, Dict
from fastapi import HTTPException
import uuid


from src.schema.pydantic_schema import QueryInput, QueryResponse, UpsertVectorRequest, Chat as ChatSchema, Message as MesssageSchema, ChatCreate, ReportMessage
from src.api.api_services import Services
from src.utils.qdrant_utils import QdrantUtils
from src.utils.audio_to_text import convert_audio_to_text
from src.utils.email_helper import EmailHelper
from src.model.db_model import Chat, Message, Base
from .db import SessionLocal, engine

from .constants import EMAIL, PASSWORD, SEND_LIST,sendgrid_api_key

Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


service = Services(qdrant_client=QdrantUtils())
app = FastAPI()
origins = [
    "http://localhost",  # Add the origins you want to allow
    "http://localhost:3000",  # Example: for a frontend running on port 3000
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict specific HTTP methods if needed
    allow_headers=["*"],  # You can restrict specific headers if needed
)

@app.get("/chats", response_model=List[ChatSchema])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chats = db.query(Chat).order_by(desc(Chat.last_message_datetime)).offset(skip).limit(limit).all()
    return [ChatSchema.from_orm(chat).dict() for chat in chats]


@app.get("/chat/{chat_id}", response_model=List[MesssageSchema])
def read_messages_for_chat(chat_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return [MesssageSchema.from_orm(message).dict() for message in messages]


@app.post("/query",response_model=MesssageSchema)
async def query(input: QueryInput,  db: Session = Depends(get_db)):
    
    output_language=input.output_language
    query_message = Message(**input.message.dict())
    chat = db.query(Chat).filter(Chat.id == query_message.chat_id).first()
    if chat:
        chat.last_message_datetime = query_message.created_at
        
    db.add(query_message)
    db.commit()
    db.refresh(query_message)
    db.refresh(chat)

    try:
        
        query_response = await service.route_user_query(query=query_message.text,chat_history=input.chat_history, output_language=output_language)
        if isinstance(query_response, dict):
            query_response = query_response.get('response')
    

        response_message = Message(text=query_response, sender="bot", chat_id=str(query_message.chat_id))
        db.add(response_message)
        db.commit()
        db.refresh(response_message)
            
        return response_message
    
    except Exception as e:
        print(e)
        db.rollback()
        return {"message" : "error", "detail" : str(e)}, 500


@app.post("/report",response_model=QueryResponse)
async def report_message(input: ReportMessage,  db: Session = Depends(get_db)):

    message = db.query(Message).filter(Message.id == input.message_id).first()

    if message is None:
        return QueryResponse(status="404", response="No message with this id found")
    
    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()

    messages = db.query(Message).filter(
        Message.chat_id == message.chat_id,
        Message.updated_at <= message.updated_at
        ).order_by(desc(Message.updated_at)).limit(11)
    # credentials_path = "/app/src/secret.json"

    email_helper = EmailHelper(sendgrid_api_key)    

    print("email class created")
    html = email_helper.create_html_for_email(messages, message, chat, input.description)
    print("email body created")
    email_helper.send_email(EMAIL, SEND_LIST, f"Issue Report : {message.id}", html)
    
    return QueryResponse(status="200", response="Chat Reported")



@app.post("/chats")
async def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    print(chat.message)

    print(chat.message.text)
    # create topic for chat
    topic_dict =  await service.topic_extraction(query=chat.message.text)

    # create chat
    db_chat = Chat(topic=topic_dict, last_message_datetime=chat.message.created_at, id=str(uuid.uuid4()))
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    # return chat and message
    return db_chat

@app.post("/post-audio", response_model=QueryResponse)
async def query(file: UploadFile = File(...)):
    
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    
    audio_input = open(file.filename, 'rb')

    message_decoded = convert_audio_to_text(audio_input)

    if not message_decoded:
        return QueryResponse(status="400",response="Can't decode a message from Audio, please record again or type a message.")
    
    return QueryResponse(status="200", response=message_decoded)

@app.post("/upsert_qdrant")
async def upsert_pinecone(input: UpsertVectorRequest):
    return await service.upsert_vectors(file_path=input.file_path,collection_name=input.collection_name)



