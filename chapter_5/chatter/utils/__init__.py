import asyncio
import threading
from queue import Queue


def async_to_sync_generator(async_gen):
    """
    Converts an async generator to a sync generator using a Queue.
    """
    # Create a Queue to communicate between async and sync
    queue = Queue()

    # Define the async task that fetches items and puts them in the queue
    async def fetch_items():
        async for item in async_gen:
            queue.put(item)
        queue.put(None)  # Signal the end of the stream

    # Start the async fetching in a background thread
    def start_background_fetching(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fetch_items())

    loop = asyncio.new_event_loop()
    threading.Thread(
        target=start_background_fetching, args=(loop,), daemon=True
    ).start()

    # Synchronously yield items from the queue
    while True:
        item = queue.get()
        if item is None:  # End of stream signal
            break
        yield item


# # Usage example assuming an async generator `async_gen_function`
# async_gen = async_gen_function()  # Replace with your actual async generator
# for item in async_to_sync_generator(async_gen):
#     print(item)
