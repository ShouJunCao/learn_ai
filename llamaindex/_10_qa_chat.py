from llamaindex._08_Vector_Store_Qdrant import index

qa_engine = index.as_query_engine()
response = qa_engine.query("Llama2 有多少参数?")

print(response)
print(1)
print(1)
print(1)
print(1)
qa_engine = index.as_query_engine(streaming=True)
response = qa_engine.query("Llama2 有多少参数?")
response.print_response_stream()

print(2)
print(2)
print(2)
print(2)

chat_engine = index.as_chat_engine()
response = chat_engine.chat("Llama2 有多少参数?")
print(response)

print(3)
print(3)
print(3)
print(3)
response = chat_engine.chat("How many at most?")
print(response)


print(4)
print(4)
print(4)
print(4)
chat_engine = index.as_chat_engine()
streaming_response = chat_engine.stream_chat("Llama 2有多少参数?")
# streaming_response.print_response_stream()
for token in streaming_response.response_gen:
    print(token, end="", flush=True)