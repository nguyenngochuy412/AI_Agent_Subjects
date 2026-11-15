from fastapi import APIRouter

router = APIRouter(tags=["chat_api"])

@router.get("/chat_api")
def chat(name: str, version: str) -> str:
    return f"Ten: {name} -- Version: {version}"
