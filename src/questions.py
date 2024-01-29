"""This module provides a class for representing the context of asking questions about a GitHub repository."""

from src.file_processing import search_documents
from src.utils import format_documents


class QuestionContext:
    """A class representing the context for asking questions about a GitHub repository.

    Attributes:
        index: The index used for searching documents.
        documents: The list of documents in the repository.
        llm_chain: The language model chain for answering questions.
        model_name: The name of the language model used.
        repo_name: The name of the GitHub repository.
        github_url: The URL of the GitHub repository.
        conversation_history: History of the conversation.
        file_type_counts: Counts of different file types in the repository.
        filenames: List of filenames in the repository.
    """

    def __init__(
        self,
        index,
        documents,
        llm_chain,
        model_name,
        repo_name,
        github_url,
        conversation_history,
        file_type_counts,
        filenames,
    ):
        """Initialize a QuestionContext object.

        Args:
            index: The index used for searching documents.
            documents: The list of documents in the repository.
            llm_chain: The language model chain for answering questions.
            model_name: The name of the language model used.
            repo_name: The name of the GitHub repository.
            github_url: The URL of the GitHub repository.
            conversation_history: History of the conversation.
            file_type_counts: Counts of different file types in the repository.
            filenames: List of filenames in the repository.
        """
        self.index = index
        self.documents = documents
        self.llm_chain = llm_chain
        self.model_name = model_name
        self.repo_name = repo_name
        self.github_url = github_url
        self.conversation_history = conversation_history
        self.file_type_counts = file_type_counts
        self.filenames = filenames


def ask_question(question, context: QuestionContext):
    """Ask a question about a GitHub repository and obtain an answer using a language model chain.

    Args:
        question (str): The user's question.
        context (QuestionContext): The context for asking the question.

    Returns:
        str: The answer to the user's question obtained from the language model chain.
    """
    relevant_docs = search_documents(
        question, context.index, context.documents, n_results=5
    )

    numbered_documents = format_documents(relevant_docs)
    question_context = f"This question is about the GitHub repository '{context.repo_name}' available at {context.github_url}. The most relevant documents are:\n\n{numbered_documents}"

    answer_with_sources = context.llm_chain.invoke(
        input={
            "model": context.model_name,
            "question": question,
            "context": question_context,
            "repo_name": context.repo_name,
            "github_url": context.github_url,
            "conversation_history": context.conversation_history,
            "numbered_documents": numbered_documents,
            "file_type_counts": context.file_type_counts,
            "filenames": context.filenames,
            "return_only_outputs": True,
        }
    )
    return answer_with_sources["text"]
