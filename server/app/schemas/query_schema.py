from pydantic import BaseModel

# class QueryParams(BaseModel):
#     directory_name: str
#     department: str
#     date_range: str

class QueryParams(BaseModel):
    tier: str
    volume: str
    date_range: str