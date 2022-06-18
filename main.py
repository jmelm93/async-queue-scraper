import random
import asyncio
import aiohttp
import requests
import time

async def worker(url, ua, session):
  
    print("Worker() - getting url: " + url)
  
  async with session.get(url, headers={'User-Agent': ua.random}) as response:
    
        html = await response.text()
      
        status = response.status     
        
        return [url, html, status]


async def scraper_queue(urlList, ua, js_render=False):
    
    url_queue = asyncio.Queue() # create queue 
    
    for url in urlList: # add all urls to queue for later processing
        await url_queue.put(url) 
        
    response = []
    
    async with aiohttp.ClientSession() as session: # create aiohttp session
            
        num_urls = len(urlList)
        i = 0

        while not url_queue.empty():
            
            range_start = i
            range_end = i + 50
            
            for j in range(range_start, range_end):
                url = await url_queue.get()
                response.append(await worker(url, session))
                i += 1
                
                print(f"{num_urls - i} urls left in queue")
                
                # break if queue is empty
                if url_queue.empty():
                    break
            
            if url_queue.empty():
                break # break loop if queue is empty

    return response
 
def main(urlList, ua):
    response = asyncio.run(
      scraper_async(
        urlList = urlList,
        ua = ua  
        js_render = True,
      )
    )

if __name__ == "__main__":
    start_full = time.time()
    main(input)
    print(f"Full job took {time.time() - start_full} seconds")
