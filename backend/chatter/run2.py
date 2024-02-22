def gen():
    for chunk in [
        "event: data\ndata: 1\n\n",
        "event: data\ndata: 2\n\n",
        "event: data\ndata: 3\n\n",
        "event: meta\n{status: 'ok'}\n\n",
    ]:
        print("about to yield", chunk)
        yield chunk
        print("yielded", chunk)
    print("**************", flush=True)
    yield "event: close\ndata: done\n\n"


for data in gen():
    print(data)
