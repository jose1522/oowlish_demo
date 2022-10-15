from worker.media.base import BaseMedia2Text
from worker.nlp.summarization import BaseSummarizer


class TextSummarizerPipeline:
    """Extracts a text summary given transcriber and summarizer objects"""

    def __init__(self, summarizer: BaseSummarizer, transcriber: BaseMedia2Text):
        """
        Creates instance of TextSummarizerPipeline
        Args:
            summarizer: instance of a BaseSummarizer subclass, like LongTextSummarizer
            transcriber: instance of a BaseMedia2Text subclass, like Youtube2Text
        """
        self.summarizer = summarizer
        self.transcriber = transcriber

    def run(self) -> str:
        """Executes the necessary steps to extract a text summary from some type of media."""
        transcript = self.transcriber.extract_text()
        return self.summarizer(transcript)
