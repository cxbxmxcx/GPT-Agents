from langchain.document_loaders import UnstructuredHTMLLoader

loader = UnstructuredHTMLLoader("sample_documents\mother_goose.html")

data = loader.load()

print(data)