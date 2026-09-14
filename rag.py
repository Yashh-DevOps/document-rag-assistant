def ask_question(question, retriever, prompt, llm, history):

    documents = retriever(question)

    context = "\n\n".join(
        [
            document.page_content
            for document in documents
        ]
    )
    conversation_history = []

    for message in history:
        role = message["role"].capitalize()
        content = message["content"]

        conversation_history.append(
        f"{role}: {content}"
    )

    conversation_history = "\n".join(conversation_history)
    messages = prompt.format_messages(
        context=context,
        question=question,
        conversation=conversation_history
    )

    response = llm.invoke(messages)

    answer = response.content

    unknown_answer = (
        "I’m sorry" in answer.lower()
        or "I'm sorry" in answer.lower()
        or "i don't know" in answer.lower()
        or "i don't have" in answer.lower()
        or "i do not know" in answer.lower()
        or "i'm not sure" in answer.lower()
        or "im not sure" in answer.lower()
        or " I couldn’t find the answer" in answer.lower()
    )

    sources = []

    if not unknown_answer:
        for document in documents:
            source = document.metadata.get(
                "source",
                "unknown source"
            )
            page = document.metadata.get("page")
            if page is not None:
                source_info = (
                    f"(source: {source}) "
                    f"(page: {page + 1})"
                )
            else:
                source_info = (
                    f"(source: {source})"
                )
            if source_info not in sources:
                sources.append(source_info)

    return answer, sources