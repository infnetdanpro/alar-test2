from quart import Quart, jsonify
import asyncio
import aiohttp

loop = asyncio.get_event_loop()
app = Quart(__name__)
app.config['JSON_SORT_KEYS'] = False


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get(url, timeout):
    conn = aiohttp.TCPConnector(limit=timeout)
    async with aiohttp.ClientSession(connector=conn) as session:
        data = await fetch(session, url)
        return data


def custom_quicksort(obj):
    if len(obj) <= 1:
        return obj
    else:
        p = obj[0]
        left = [i for i in obj[1:] if i['id'] <= obj[0]['id']]
        right = [i for i in obj[1:] if i['id'] > obj[0]['id']]
        # print(p, left, right)
        return custom_quicksort(left) + [p] + custom_quicksort(right)


# Views
@app.route('/')
async def index():
    timeout = 2
    url_a = 'http://127.0.0.1:5000/static/file_a.json'
    url_b = 'http://127.0.0.1:5000/static/file_b.json'
    # url_c = ''
    # add new get function to gather
    response = await asyncio.gather(
        get(url_a, timeout),
        get(url_b, timeout)
    )
    obj = []
    for block in response:
        for elem in block:
            obj.append(elem)

    response = sorted(obj, key=lambda x: x['id'])
    # or custom quicsort for object
    # response = custom_quicksort(obj)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
