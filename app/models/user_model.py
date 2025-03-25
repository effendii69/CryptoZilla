from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type='string')
        return json_schema

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    wallet_id: str
    password: str

    class Config:
        json_encoders = {
            ObjectId: str
        }
        populate_by_name = True
