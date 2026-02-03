from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
from loguru import logger


client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None

async def connect_to_mongo():
    """create database connection"""
    global client, database
    try:
        # For MongoDB Atlas, ensure SSL/TLS is properly configured
        # Motor automatically uses TLS for mongodb+srv:// connections
        # The connection string should already include SSL parameters
        client = AsyncIOMotorClient(
            settings.MONGO_URL,
            serverSelectionTimeoutMS=30000,  # 30 seconds timeout
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            # TLS is automatically enabled for mongodb+srv:// connections
            # System CA certificates (installed via ca-certificates package) will be used
        )
        database = client[settings.DB_NAME]
        # Test connection
        await client.admin.command('ping')
        logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise

async def close_mongo_connection():
    """close database connection"""
    global client
    if client:
        client.close()
        logger.info("🔌 MongoDB connection closed")

async def get_database() -> AsyncIOMotorDatabase:
    """get database connection"""
    return database

