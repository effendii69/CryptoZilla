from fastapi import APIRouter, HTTPException
from ..api_integration import get_stock_data

api_router = APIRouter()

@api_router.get("/stock/{symbol}")
async def fetch_stock_data(symbol: str):
    try:
        data = get_stock_data(symbol)
        if "Error" in data:
            raise HTTPException(status_code=400, detail=data["Error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
