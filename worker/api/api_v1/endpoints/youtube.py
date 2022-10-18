import json

from fastapi import APIRouter, WebSocket
from pydantic import ValidationError
from youtube_transcript_api import TranscriptsDisabled

from core import logger
from core.pipeline import TextSummarizerPipeline
from media.online import Youtube2Text
from nlp.summarization import LongTextSummarizer
from schemas import media, summary

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
    logger.info("Awaiting connection on socket")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info("Received data from client via socket.")
            parsed_data = media.OnlineSource(
                **json.loads(data)
            )  # type: media.OnlineSource
            logger.info(f"Request params {parsed_data.dict()}")
            logger.info("Performing inference")
            pipeline = TextSummarizerPipeline(
                summarizer=LongTextSummarizer(),
                transcriber=Youtube2Text(source=parsed_data.url),
            )
            output = {
                "summary": pipeline.run(
                    max_length=parsed_data.max_length, min_length=parsed_data.min_length
                )
            }
            await websocket.send_json(output)
    # See websocket error codes:
    # https://www.iana.org/assignments/websocket/websocket.xhtml
    except ValidationError as error:
        await websocket.close(code=1007, reason="invalid payload structure")
        logger.error(error.json())
    except TranscriptsDisabled as error:
        await websocket.close(code=1007, reason="could not get transcript for video")
        logger.error(str(error))
