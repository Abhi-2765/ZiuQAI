class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def as_retriever(self, k: int = 4):
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )
