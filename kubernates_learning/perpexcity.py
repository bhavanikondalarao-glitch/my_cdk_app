#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

import getpass
import os

os.environ["PPLX_API_KEY"] = "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"

#if not os.environ.get("PPLX_API_KEY"):
  #os.environ["PPLX_API_KEY"] = getpass.getpass("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")

from langchain.chat_models import init_chat_model

model = init_chat_model("llama-3.1-sonar-small-128k-online", model_provider="perplexity")
model.invoke("Hello, world!")