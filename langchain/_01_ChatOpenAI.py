from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_verbose, set_debug, set_llm_cache
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())



# 设置全局 verbose
set_verbose(True)

# 获取当前的 debug 设置
#old_debug = get_debug()

# 设置新的 debug 值（如果需要的话）
set_debug(True)

# 获取当前的 LLM 缓存
#old_llm_cache = get_llm_cache()

# 设置新的 LLM 缓存（如果需要的话）
new_cache = InMemoryCache()
set_llm_cache(new_cache)

llm = ChatOpenAI(model="gpt-4o-mini", verbose=True)  # 默认是gpt-3.5-turbo

if __name__ == "__main__":
    response = llm.invoke("你是谁")
    print(response.content)
