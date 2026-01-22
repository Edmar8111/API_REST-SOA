from . import main
import uvicorn


async def app(
  scope, received, send      
):
    await send({
        'type':'http.response.start',
        'status':200,
        'headers':[
            (b'content-type',b'text/plain'),
            (b'content-length',b'13'),
        ]
    })
    await send({
        'type':'htpp.response.body',
        'body':b'Hello, World'
    })

