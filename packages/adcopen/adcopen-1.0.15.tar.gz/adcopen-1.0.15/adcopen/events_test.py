
from events import Events

import asyncio

class TestClass(object):

    def __init__(self):
        Events.subscribe_method("evtest",self.myInternal)

    async def myInternal(self, data):
        print(f"Internal callback:{data}")







@Events.subscribe("evtest")
async def myExternal(data):
    print(f"External callback:{data}")

@Events.subscribe("evtest")
def mySync(data):
    print(f"Synchronous callback:{data}")
    #f = 12 / 0



@Events.subscribe("sec-test")
async def mySec(data):
    print(f"Second :{data}")


@Events.subscribe("third-test")
async def myThird(data):
    print(f"Third :{data}")

tc = TestClass()


try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

Events.publish("evtest", "The quick brown fox yada yada yada.")

Events.publish("sec-test", "This is the second.")

Events.publish("third-test", "This is the third.")


try:

    loop.run_forever()  
        
except KeyboardInterrupt:
    
    print( "Closing from keyboard request.")  




