from fastapi import Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from logger import logger

async def catch_exception_middleware(request:Request,call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("Exception is not handled")
        return JSONResponse(
            status_code=500,
            content={"error":str(exc)}
        )