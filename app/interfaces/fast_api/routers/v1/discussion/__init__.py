from fastapi import APIRouter

from .discussion import router as discussion_router
from .discussion_attachment import router as discussion_attachment_router
from .discussion_message import router as discussion_message_router

router = APIRouter(tags=["v1/discussion"])
router.include_router(discussion_router)
router.include_router(discussion_message_router)
router.include_router(discussion_attachment_router)

