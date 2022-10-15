import json

from fastapi import APIRouter, WebSocket, status
from pydantic import ValidationError

from worker.core.pipeline import TextSummarizerPipeline
from worker.media.online import Youtube2Text
from worker.nlp.summarization import LongTextSummarizer
from worker.schemas import media, summary

router = APIRouter()


@router.post("/", response_model=summary.TextSummary)
async def get_text_summary(data: media.OnlineSource):
    """HTTP endpoint for receiving Youtube link videos and sending back a summary of it."""
    pipeline = TextSummarizerPipeline(
        summarizer=LongTextSummarizer(), transcriber=Youtube2Text(source=data.url)
    )
    return {"summary": pipeline.run()}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket for receiving Youtube link videos and sending back a summary of it."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()

            parsed_data = media.OnlineSource(
                **json.loads(data)
            )  # type: media.OnlineSource
            pipeline = TextSummarizerPipeline(
                summarizer=LongTextSummarizer(),
                transcriber=Youtube2Text(source=parsed_data.url),
            )
            output = {"summary": pipeline.run()}

            await websocket.send_text(json.dumps(output))
    except ValidationError as error:
        await websocket.close(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY, reason=error.json()
        )
