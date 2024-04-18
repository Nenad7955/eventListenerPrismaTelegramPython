import asyncio

from datetime import datetime
from web3 import Web3
from web3.contract import Contract
from web3.contract.contract import ContractEvent

from db import EventRepository

web3: Web3
contract: Contract
event_filter: ContractEvent
event_repository: EventRepository


def main(infura_url, contract_address, event_repo):
    global web3, contract, event_filter, event_repository
    web3 = Web3(Web3.WebsocketProvider(infura_url))
    contract = web3.eth.contract(address=contract_address, abi=abi)
    event_filter = contract.events.TotalDistribution.create_filter(toBlock='latest', fromBlock=19661801)
    event_repository = event_repo


async def handle_event(event):
    timestamp = web3.eth.get_block(event.blockNumber).timestamp
    print(timestamp)
    try:
        await event_repository.save_event(
            event['args']['inputAixAmount'],
            event['args']['distributedAixAmount'],
            event['args']['swappedEthAmount'],
            event['args']['distributedEthAmount'],
            timestamp,
            event['transactionHash'].hex(),
        )
    except Exception as e:
        print(e)


async def listen_for_events():
    while True:
        for event in event_filter.get_new_entries():
            await handle_event(event)
        await asyncio.sleep(2)  # Adjust the polling interval as needed


#should add hash so to not add duplicates
async def get_historic_events():
    try:
        historic_events = event_filter.get_all_entries()
        for event in historic_events:
            await handle_event(event)
    except Exception as e:
        print(e)

abi = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "inputAixAmount",
            "type": "uint256"
        },
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "distributedAixAmount",
            "type": "uint256"
        },
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "swappedEthAmount",
            "type": "uint256"
        },
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "distributedEthAmount",
            "type": "uint256"
        }
    ],
    "name": "TotalDistribution",
    "type": "event"
}]
