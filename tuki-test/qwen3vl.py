from ollama import chat
from ollama import ChatResponse

# stream = chat(
#     model='qwen3-vl:2b',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,
# )
# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)

response: ChatResponse = chat(
	# model='qwen3-vl:235b-cloud', 
  model='qwen3-vl:2b',
	messages=[
  {
    'role': 'user',
    'content': 'What is this?',
    # 'images': ['/home/tukilp21/Desktop/FM_testing/scene1.png'],
  },
  ],
  think=False,
)
# NOTE: without streaming
print(response.message.thinking)
print("----------------------------")
print(response.message.content)[phanl@m3-login1 mh42]$ pwd
/home/phanl/mh42

# REFERENCE
'''
https://github.com/ollama/ollama-python/blob/main/ollama/_types.py#L283
'''
