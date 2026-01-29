import main
import uvicorn


async def app(
  scope, received, send      
):
    await send({
        'type':'http.response.start',
        'status':200,
        'headers':[
            (b'content-type',b'text/plain'),
            (b'content-length',b'12'),
        ]
    })
    await send({
        'type':'http.response.body',
        'body':b'Hello, World'
    })

