from jina import Client, DocumentArray

if __name__ == "__main__":
    jina_client = Client(host="grpc://0.0.0.0:54321")
    da = DocumentArray().empty(2)
    da.texts = ["hello", "world!!"]
    da_res = jina_client.post("/", da)
    print(da_res.embeddings)
    print(type(da_res.embeddings))

    da_res = jina_client.post("/current_model")
    print(da_res.texts)
