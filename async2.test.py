import asyncio
import random
import functools
import smbus
import time

def get_fTemp():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    return(str(round(fTemp, 2)))

def get_humidity():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    return(str(round(humidity, 2)))

# make the print function always flush output immediately
# without this you'll find nothing gets printed until program
# end when suddenly all output is printed at once
print = functools.partial(print, flush=True)

# A message to indicate end of processing, the purpose of this
# will become clear in the examples
END_OF_QUEUE = "This is the end...  This value doesn't actually matter so long as it's not a possible real value to go in the queue"
def make_random():
    return(fandom.randint(0,100))


async def producer_hum(queue):
    while True:
        try:
            msg = make_random()
        except IOError:
            msg = END_OF_QUEUE
        topic = "homeassistant/thermostat/humidity"
        print(topic, msg)
        pack = {"topic": topic, "message": msg}
        await asyncio.sleep(10)
        await queue.put(pack)

async def producer_temp(queue):
	    while True:
        try:
            msg = random.random(0.00)
        except IOError:
            msg = END_OF_QUEUE
        topic = "homeassistant/thermostat/tempature"
        print(topic, msg)
        pack = {"topic": topic, "message": msg}
        await queue.put(pack)
        await asyncio.sleep(10)


async def consumer(queue):
    while True:
        data = await.queue.get()
        if data["message"] == END_OF_QUEUE:
            print("something wetn wrong with pulling humidity ending task")
            break
        print(f"topic: {topic}, message: {message}")
        client.publish(topic, message)
        await asyncio.sleep(5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    loop.run_until_complete(asyncio.gather(producer_hum(queue),producer_temp(queue), consumer(queue)))
    loop.stop()
    loop.close()



# 
# async def producer(queue):
#     while True:
#         emit_me = random.randint(1, 42)
#         if emit_me == 42:
#             print("At the end")
#             break
#         else:
#             msg = f"Emitting {emit_me}"
#             print(msg)
#             # simulate some IO time
#             await asyncio.sleep(random.uniform(0, 0.5))
#             await queue.put(msg)
#
#     await queue.put(END_OF_QUEUE)
#
#
# async def consumer(queue):
#     while True:
#         message = await queue.get()
#         if message == END_OF_QUEUE:
#             print(f"This is the end my friend....")
#             break
#         print(f"Got message: {message}")
#         # simulate some IO time
#         await asyncio.sleep(random.uniform(0, 1.0))
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     queue = asyncio.Queue()
#     loop.run_until_complete(asyncio.gather(producer(queue), consumer(queue)))
#     loop.stop()
#     loop.close()
