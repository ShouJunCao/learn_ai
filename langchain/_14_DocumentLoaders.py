from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("llama2.pdf")
pages = loader.load_and_split()

print(pages[0].page_content)