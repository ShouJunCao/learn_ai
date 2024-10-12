from langchain_core.prompts import PromptTemplate
import _01_ChatOpenAI

template = PromptTemplate.from_template("给我讲个关于{subject}的笑话")

if __name__ == '__main__':
    print("===Template===")
    print(template)
    print("===Prompt===")
    print(template.format(subject='小明'))