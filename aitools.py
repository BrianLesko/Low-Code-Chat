from openai import OpenAI
try:
  from keys import xai_api_key, openai_api_key
except:
  xai_api_key = ''
  openai_api_key = ''
  print("No API key found in keys.py")
import os

class AIClient:

  def __init__(self,ai_company_name,api_key=None):
    self.ai_company_name = ai_company_name
    self._set_environment_variables()
    if api_key: # If an API key is provided, use it instead of what is defined in _get_environment_variables
      self.api_key = api_key
      os.environ['API_KEY'] = self.api_key
    self.client = OpenAI(api_key=self.api_key,base_url=self.base_url)

  def _set_environment_variables(self):

    if self.ai_company_name == 'xai':
      # XAI API Key
      self.api_key = xai_api_key
      self.model_name = 'grok-beta'
      self.base_url="https://api.x.ai/v1"

    if self.ai_company_name == 'openai':
      # OpenAI API Key
      self.api_key = openai_api_key
      self.model_name = 'gpt-4o'
      self.base_url="https://api.openai.com/v1"

    if self.ai_company_name not in ['xai','openai']:
      raise ValueError(f"No API configuration found for {self.ai_company_name}")

    os.environ['API_KEY'] = self.api_key
    os.environ['MODEL_NAME'] = self.model_name
    os.environ['BASE_URL'] = self.base_url

  def get_stream(self,messages):
    self.messages = messages
    stream = self.client.chat.completions.create(model=self.model_name, messages=self.messages, stream=True)
    return stream
  
  def reset_api_key(self,key):
    self.api_key = key
    os.environ['API_KEY'] = self.api_key
    self.client = OpenAI(api_key=self.api_key,base_url=self.base_url)
    return self.api_key