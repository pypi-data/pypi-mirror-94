import aiohttp
import json

API_BASE_URL = "https://lichess.org"

async def stream(endpoint, token):  
  i = 0
  async with aiohttp.request('get', f'{API_BASE_URL}/{endpoint}', headers={"Authorization":f'Bearer {token}'}) as r:
    async for line in r.content:              
      try:
        blob = json.loads(line)
      except:
        blob = {}
      print(i, line, blob)      
      i += 1