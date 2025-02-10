import os
import openai
import logging
import tiktoken

from dotenv import load_dotenv
from typing import List, Tuple

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Constants
TOKEN_CONSTANT = 1000
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 3000))
OPEN_AI_PRICE = float(os.getenv("OPEN_AI_PRICE", 0.002))
ENCODING_TYPE = os.getenv("ENCODING_TYPE", "cl100k_base")
MODEL_ENGINE = os.getenv("OPENAI_MODEL_ENGINE", "gpt-3.5-turbo")
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY


class OpenAI_Summarizer:
    """
    A class for summarizing podcast transcripts using OpenAI's GPT models.
    """

    def __init__(self, max_sentences: int = 15):
        """
        Initialize the summarizer with the maximum number of sentences in the final summary.
        """
        self.max_sentences = max_sentences

    def summarize(self, transcribed_text: str) -> Tuple[str, float]:
        """
        Summarizes the full transcribed text by first chunking it, then generating partial summaries,
        and finally producing a final concise summary.
        """
        chunks = self._split_into_chunks(transcribed_text)
        partial_summaries, tokens_used = self._summarize_chunks(chunks)

        combined_summary = "\n\n".join(partial_summaries)
        final_prompt = f"""
            Instructions:
            Summarize the following podcast text into a list of {self.max_sentences} sentences
            Contextualize the topics to the podcast
            Don't mention the podcast itself in the summary.

            Text: {combined_summary}

            Summary:
        """

        summary, token_count = self._call_openai(final_prompt)
        tokens_used += token_count

        api_cost = float(tokens_used / TOKEN_CONSTANT) * OPEN_AI_PRICE
        return summary, api_cost

    def _num_tokens_from_string(self, text: str) -> int:
        """
        Returns the number of tokens in a given text string.
        """
        encoding = tiktoken.get_encoding(ENCODING_TYPE)
        return len(encoding.encode(text))

    def _split_into_chunks(self, transcript: str) -> List[str]:
        """
        Splits the transcript into chunks based on token limits.
        """
        chunks, buffer, token_count = [], "", 0

        sentences = transcript.split(".")
        for sentence in sentences:
            num_tokens = self._num_tokens_from_string(sentence)
            token_count += num_tokens
            buffer += sentence + "."

            if token_count > CHUNK_SIZE:
                chunks.append(buffer)
                buffer = ""
                token_count = 0

        if buffer:
            chunks.append(buffer)

        logger.info(f"Created {len(chunks)} chunks from transcript.")
        return chunks

    def _call_openai(self, prompt: str) -> Tuple[str, int]:
        """
        Calls the OpenAI API with a prompt and returns the response along with token usage.
        """
        response = openai.chat.completions.create(
            model=MODEL_ENGINE,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that summarizes podcasts.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        choices = response.choices

        if choices:
            content = choices[0].message.content
            total_tokens = response.usage.total_tokens
            return content, total_tokens
        else:
            logger.error("No response choices received from OpenAI API.")
            raise RuntimeError("Failed to retrieve a summary from OpenAI API.")

    def _summarize_chunks(self, chunks: List[str]) -> Tuple[List[str], int]:
        """
        Processes chunks through OpenAI API to generate summaries.
        """
        summaries, total_tokens = [], 0

        for chunk in chunks:
            prompt = f"""
                Summarize the following podcast partial transcript into sentences:

                {chunk}

                Summary:
            """
            summary, token_count = self._call_openai(prompt)
            total_tokens += token_count
            summaries.append(summary)

        return summaries, total_tokens
