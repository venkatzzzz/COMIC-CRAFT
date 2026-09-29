from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.templating import Jinja2Templates

from .schemas import PromptRequest
from .services.comic_service import generate_comic
from .ai.gemini_flash import generate_image


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/")
async def home(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.post("/generate")
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style
        )

        result = generate_comic(
            payload
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context=result
        )



@router.post(
    "/generate-comic/json"
)
async def generate_json(
    payload: PromptRequest
):
    try:

        return generate_comic(
            payload
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@router.post("/test-image")
async def test_image(
    prompt: str = Form(...)
):
    try:

        image_url = generate_image(
            prompt,
            0
        )

        return {
            "image_url": image_url
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@router.get("/export-success")
async def export_success(
    request: Request,
    pdf_url: str = ""
):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_url": pdf_url
        }
    )


@router.get("/health")
async def health():

    return {
        "status": "ok"
    }