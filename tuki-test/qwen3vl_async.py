import asyncio
from ollama import chat

MODEL = 'qwen3-vl:2b'

async def stream_chat(model, messages, think=True):
    """Simpler async wrapper around the blocking `chat(..., stream=True)`.

    This version avoids type annotations and keeps the same thread+queue
    approach so you can `async for` streaming chunks.
    """
    loop = asyncio.get_running_loop()
    q = asyncio.Queue()

    def producer():
        try:
            for chunk in chat(model=model, messages=messages, stream=True, think=think):
                loop.call_soon_threadsafe(q.put_nowait, chunk)
        finally:
            loop.call_soon_threadsafe(q.put_nowait, None)

    loop.run_in_executor(None, producer)

    while True:
        chunk = await q.get()
        if chunk is None:
            break

        # support dict or object shapes from the library
        msg = chunk.get("message") if isinstance(chunk, dict) else getattr(chunk, "message", None)
        if not msg:
            continue

        thinking = msg.get("thinking") if isinstance(msg, dict) else getattr(msg, "thinking", None)
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", None)

        yield thinking, content


async def main():
    messages = [
        {"role": "user", 
        "content": "What is this?"
        }
    ]

    async for thinking, content in stream_chat(MODEL, messages, think=True):
        if thinking is not None:
            print(f"[thinking={thinking}]", end="", flush=True)
        if content:
            print(content, end="", flush=True)

    print("\n--- done ---")


if __name__ == "__main__":
    asyncio.run(main())
