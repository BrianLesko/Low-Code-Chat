from openai import OpenAI
import json
import os
from PIL import Image
import io
import base64

keys = json.load(open("keys.json"))
xai_api_key = keys.get('xai_api_key', None)
openai_api_key = keys.get('openai_api_key', None)

class AIClient:

  def __init__(self,company_name,api_key=None):
    self.company_name = company_name

    # check for API key in keys.json
    if company_name == 'xai' and xai_api_key is not None:
      self.api_key = xai_api_key
    elif company_name == 'openai' and openai_api_key is not None:
      self.api_key = openai_api_key
    elif api_key is not None:
      self.api_key = api_key
    else:
      self.api_key = None

    #if api_key: # If an API key is provided, use it instead of what is defined in _get_environment_variables
    #  os.environ['API_KEY'] = self.api_key

  def setup(self):
    self._set_environment_variables()
    self._get_client()

  def _get_client(self):
    self.client = OpenAI(api_key=self.api_key,base_url=self.base_url)

  def _set_environment_variables(self):

    if self.company_name == 'xai':
      # XAI API Key
      self.api_key = xai_api_key
      self.model_name = 'grok-beta'
      self.base_url="https://api.x.ai/v1"

    if self.company_name == 'openai':
      # OpenAI API Key
      self.api_key = openai_api_key
      self.model_name = 'gpt-4o'
      self.base_url="https://api.openai.com/v1"

    if self.company_name not in ['xai','openai']:
      raise ValueError(f"No API configuration found for {self.company_name}")

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
  
  def _reduce_image_size(self, upload, quality=80, width=255, height=255, center_crop=True):
    image = Image.open(upload)
    min_dim = min(image.size)
    if center_crop: image = image.crop(((image.width - min_dim) // 2, (image.height - min_dim) // 2, (image.width + min_dim) // 2, (image.height + min_dim) // 2))
    image = image.resize((width, height))
    image = image.convert("RGB")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=quality)  # Quality can be adjusted
    return base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")  # Convert to Base64 and decode to string