import asyncio
import os

from dotenv import load_dotenv
from prisma import Prisma

import telegram_bot
import blockchain
import db

load_dotenv()

contract_address = os.getenv("CONTRACT_ADDRESS")
infura_url = os.getenv("INFURA_URL")
telegram_api_key = os.getenv("TELEGRAM_API")

    
def main():

    prsm = Prisma()
    asyncio.run(prsm.connect())

    event_repository = db.EventRepository(prsm)

    telegram_bot.main(telegram_api_key, event_repository)
    blockchain.main(infura_url, contract_address, event_repository)

    asyncio.run(blockchain.get_historic_events())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            asyncio.gather(
                telegram_bot.send(),
                blockchain.listen_for_events()
            )
        )
    finally:
        loop.close()


if __name__ == "__main__":
    main()
