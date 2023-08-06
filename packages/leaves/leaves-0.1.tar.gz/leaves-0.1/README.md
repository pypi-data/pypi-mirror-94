# leaves

python+rabbitmq 的rpc 调用封装

## 目的

1. 希望能够完成一个微小的，便于使用的，基于rabbitmq 的rpc 调用；
1. 内部核心处理，能够以插拔的形式修改，相对于nameko的使用，结果队列是链接断开就删除的这些特殊要求便于实现；
1. 依赖少，以为微服务rpc调用做准备，便于docker镜像打包，甚至希望能够便于编译打包，以scratch 镜像运行；
1. 以asynico 异步为核心实现；

### rpc 客户端使用

```python


import asyncio

from leaves import RPC, RabbitmqConfig


async def main():
    config = RabbitmqConfig(con_url="amqp://")
    async with RPC(config) as rpc:
        rpc: RPC
        data = await rpc.points.hello("test", a="345")
        print(data)
    async with RPC(config) as rpc:
        rpc: RPC
        data = await rpc.kinds.call("test", a="345")
        print(data)
    print("结束")


asyncio.ensure_future(main())
asyncio.get_event_loop().run_forever()

```

### 服务端使用

```python

import asyncio
from leaves import RPC, RabbitmqConfig, Leaf, MicroContainer,service_publish

config = RabbitmqConfig(con_url="amqp://")

leaf = Leaf("points")
leaf2 = Leaf("kinds")


@leaf.rpc
async def hello(*args, **kwargs):
    print("函数被调用了")
    return 1


@leaf2.rpc
async def call(*args, **kwargs):
    return "call"


container = MicroContainer([leaf, leaf2], config)

asyncio.ensure_future(service_publish(container))
asyncio.get_event_loop().run_forever()

```
