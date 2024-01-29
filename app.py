"""Entrypoint for git-llm-analyzer."""

import os
import tempfile

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama

from src.config import GREEN, RESET_COLOR, WHITE
from src.file_processing import clone_github_repo, load_and_index_files
from src.questions import QuestionContext, ask_question
from src.utils import format_user_question

load_dotenv()


def main():
    """Main function to interactively ask questions about a GitHub repository.

    This function prompts the user to enter the GitHub URL of a repository,
    clones the repository, indexes its files, and allows the user to ask
    questions interactively with a language model chain.

    Args:
        None

    Returns:
        None
    """
    github_url = input("Enter the GitHub URL of the repository: ")
    repo_name = github_url.split("/")[-1]
    print("Cloning the repository...")
    with tempfile.TemporaryDirectory() as local_path:
        if clone_github_repo(github_url, local_path):
            index, documents, file_type_counts, filenames = load_and_index_files(
                local_path
            )
            if index is None:
                print("No documents were found to index. Exiting.")
                exit()

            print("Repository cloned. Indexing files...")
            llm = Ollama(model=os.getenv("OLLAMA_MODEL"), verbose=True)

            template = """
            Repo: {repo_name} ({github_url}) | Conv: {conversation_history} | Docs: {numbered_documents} | Q: {question} | FileCount: {file_type_counts} | FileNames: {filenames}

            Instr:
            1. Answer based on context/docs.
            2. Focus on repo/code.
            3. Consider:
                a. Purpose/features - describe.
                b. Functions/code - provide details/samples.
                c. Setup/usage - give instructions.
            4. Unsure? Say "I am not sure".

            Answer:
            """

            prompt = PromptTemplate(
                template=template,
                input_variables=[
                    "repo_name",
                    "github_url",
                    "conversation_history",
                    "question",
                    "numbered_documents",
                    "file_type_counts",
                    "filenames",
                ],
            )

            llm_chain = LLMChain(prompt=prompt, llm=llm)

            conversation_history = ""
            question_context = QuestionContext(
                index,
                documents,
                llm_chain,
                os.getenv("OLLAMA_MODEL"),
                repo_name,
                github_url,
                conversation_history,
                file_type_counts,
                filenames,
            )
            while True:
                try:
                    user_question = input(
                        "\n"
                        + WHITE
                        + "Ask a question about the repository (type 'exit()' to quit): "
                        + RESET_COLOR
                    )
                    if user_question.lower() == "exit()":
                        break
                    print("Thinking...")
                    user_question = format_user_question(user_question)

                    answer = ask_question(user_question, question_context)
                    print(GREEN + "\nANSWER\n" + answer + RESET_COLOR + "\n")
                    conversation_history += (
                        f"Question: {user_question}\nAnswer: {answer}\n"
                    )
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        else:
            print("Failed to clone the repository.")


if __name__ == "__main__":
    main()
