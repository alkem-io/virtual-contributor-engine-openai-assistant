# from langchain_core.pydantic_v1 import SecretStr
from config import LOG_LEVEL

# from langchain_openai import ChatOpenAI


# verbose output for LLMs
if LOG_LEVEL == "DEBUG":
    verbose_models = True
else:
    verbose_models = False


# models_map = {"generic-openai": ChatOpenAI}


# def get_model(engine, api_key):
#     model_class = models_map[engine]
#     model = model_class(
#         model="gpt-4o",
#         temperature=0,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#         api_key=SecretStr(api_key),
#     )
#     return model
