DISTANCE_THRESHOLD = 1.0


def create_retriever(vector_store):

    def retrieve_documents(question):

        results = vector_store.similarity_search_with_score(
            question,
            k=4
        )

        filtered_documents = []

        for document, score in results:

            if score <= DISTANCE_THRESHOLD:
                filtered_documents.append(document)

        return filtered_documents

    return retrieve_documents