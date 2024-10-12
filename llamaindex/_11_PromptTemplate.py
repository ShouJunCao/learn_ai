from llama_index.core import PromptTemplate

prompt = PromptTemplate("写一个关于{topic}的笑话")

str = prompt.format(topic="小明")

if __name__ == '__main__':
    print(str)