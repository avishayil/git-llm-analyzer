"""Utility functions for text processing and formatting."""

import os
import re

import nltk

nltk.download("punkt")


def clean_and_tokenize(text):
    """Clean and tokenize the input text.

    This function performs various cleaning steps on the input text, such as
    removing HTML tags, special characters, URLs, and digits. It then tokenizes
    the cleaned text into words.

    Args:
        text (str): The input text.

    Returns:
        list: A list of tokens representing the cleaned and tokenized text.
    """
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"\b(?:http|ftp)s?://\S+", "", text)
    text = re.sub(r"\W", " ", text)
    text = re.sub(r"\d+", "", text)
    text = text.lower()
    return nltk.word_tokenize(text)


def format_documents(documents):
    """Format a list of documents for display.

    This function formats a list of documents by adding numbers and
    concatenating document names and content.

    Args:
        documents (list): A list of documents.

    Returns:
        str: A formatted string representing the documents.
    """
    numbered_docs = "\n".join(
        [
            f"{i+1}. {os.path.basename(doc.metadata['source'])}: {doc.page_content}"
            for i, doc in enumerate(documents)
        ]
    )
    return numbered_docs


def format_user_question(question):
    """Format a user's question.

    This function trims leading and trailing whitespaces from the user's question.

    Args:
        question (str): The user's question.

    Returns:
        str: The formatted user's question.
    """
    question = re.sub(r"\s+", " ", question).strip()
    return question
