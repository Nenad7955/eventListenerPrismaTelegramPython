from prisma import Prisma
from datetime import datetime

class EventRepository:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def save_event(self, aixProcessed, aixDistributed, ethProcessed, ethDistributed, timestamp, txhash):
        try:
            return await self.prisma.event.create({
                "aixProcessed": str(aixProcessed),
                "aixDistributed": str(aixDistributed),
                "ethProcessed": str(ethProcessed),
                "ethDistributed": str(ethDistributed),
                "timestamp": timestamp,
                "txhash": txhash
            })
        except Exception as e:
            print(e)

    async def get_all_events_last_24h(self):
        current_time = int(datetime.now().timestamp())
        try:
            return await self.prisma.event.find_many(
                where={
                    'timestamp': {
                        'gt': current_time - 60*60*24
                    }
                }
            )
        except Exception as e:
            print(e)
            return await self.get_all_events_last_24h()
