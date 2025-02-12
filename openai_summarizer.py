import os
import logging

from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
from utils.openai_utils import (
    chunk_on_delimiter,
    get_chat_completion,
    num_tokens_from_text,
)

load_dotenv()

logger = logging.getLogger(__name__)


class OpenAI_Summarizer:
    """
    A class for summarizing podcast transcripts using OpenAI's GPT models.
    """

    def __init__(self, config: dict):
        """
        Initializes the OpenAI Summarizer.

        Parameters:
        - config (dict): Configuration dictionary containing settings, including whether debugging is enabled.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = config
        self.debug = self.config.get("DEBUG", False)

    def summarize(
        self,
        text: str,
        detail: float = 0,
        additional_instructions: Optional[str] = None,
        minimum_chunk_size: Optional[int] = 500,
        chunk_delimiter: str = ".",
    ):
        """
        Summarizes a given text by splitting it into chunks and summarizing each individually.

        Parameters:
        - text (str): The text to be summarized.
        - detail (float, optional): Value between 0 and 1 indicating the level of detail (0 = highly summarized, 1 = detailed). Defaults to 0.
        - additional_instructions (Optional[str], optional): Additional custom instructions for the summarization.
        - minimum_chunk_size (Optional[int], optional): Minimum chunk size for splitting text. Defaults to 500 tokens.
        - chunk_delimiter (str, optional): Delimiter used to split the text into chunks. Defaults to ".".

        Returns:
        - str: The final compiled summary of the text.
        """
        # Ensure detail value is within valid range
        assert 0 <= detail <= 1

        # Determine number of chunks dynamically based on the desired detail level
        min_chunks = 1
        max_chunks = len(
            chunk_on_delimiter(text, minimum_chunk_size, chunk_delimiter, self.debug)
        )
        num_chunks = int(min_chunks + detail * (max_chunks - min_chunks))

        # Calculate chunk size based on total document length and target chunk count
        document_length = num_tokens_from_text(text)
        chunk_size = max(minimum_chunk_size, document_length // num_chunks)
        text_chunks = chunk_on_delimiter(text, chunk_size, chunk_delimiter, self.debug)

        if self.debug:
            logger.info(
                f"Splitting the text into {len(text_chunks)} chunks to be summarized."
            )
            logger.info(
                f"Chunk lengths are {[num_tokens_from_text(x) for x in text_chunks]}"
            )

        # Construct system message
        system_message_content = "Rewrite this text in summarized form."
        if additional_instructions is not None:
            system_message_content += f"\n\n{additional_instructions}"

        # Summarize each chunk individually and accumulate results
        accumulated_summaries = []
        for chunk in text_chunks:
            messages = [
                {"role": "system", "content": system_message_content},
                {"role": "user", "content": chunk},
            ]
            response = get_chat_completion(self.client, messages)
            accumulated_summaries.append(response)

        # Compile final summary from individual chunk summaries
        final_summary = "\n\n".join(accumulated_summaries)

        return final_summary
