from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader

reader = SimpleDirectoryReader(
        input_dir="./data", # 目标目录
        recursive=False, # 是否递归遍历子目录
        required_exts=[".pdf"], # (可选)只读取指定后缀的文件
        file_extractor={".pdf": PyMuPDFReader()} # 指定特定的文件加载器
    )

documents = reader.load_data()

print(documents[0].text)