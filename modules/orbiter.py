import random
import sys
from typing import Union

from loguru import logger
from web3 import Web3

from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import ORBITER_CONTRACT


class Orbiter(Account):
    def __init__(self, account_id: int, private_key: str, chain: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain=chain)

        self.bridge_codes = {
            "ethereum": 9001,
            "arbitrum": 9002,
            "polygon": 9006,
            "optimism": 9007,
            "zksync": 9014,
            "bsc": 9015,
            "nova": 9016,
            "zkevm": 9017,
        }

    def get_tx_data(self, value: float, destination_chain: str):
        amount = int(Web3.to_wei(value, "ether") + self.bridge_codes[destination_chain])

        tx = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "to": Web3.to_checksum_address(ORBITER_CONTRACT),
            "value": amount,
            "gasPrice": self.w3.eth.gas_price,
            "from": self.address
        }
        return tx

    @retry
    @check_gas
    def bridge(self, destination_chain: str, min_bridge: float, max_bridge: float, decimal: int):
        amount = round(random.uniform(min_bridge, max_bridge), decimal)

        if amount < 0.005 or amount > 5:
            logger.error(
                f"[{self.account_id}][{self.address}] Limit range amount for bridge 0.005 – 5 ETH | {amount} ETH"
            )
            sys.exit()

        logger.info(f"[{self.account_id}][{self.address}] Bridge {self.chain} –> {destination_chain} | {amount} ETH")

        tx_data = self.get_tx_data(amount, destination_chain)
        balance = self.w3.eth.get_balance(self.address)

        if tx_data["value"] >= balance:
            logger.error(f"[{self.account_id}][{self.address}] Insufficient funds!")
        else:
            gas_limit = self.w3.eth.estimate_gas(tx_data)
            tx_data.update({'gas': gas_limit})

            signed_txn = self.sign(tx_data)

            txn_hash = self.send_raw_transaction(signed_txn)

            res = self.wait_until_tx_finished(txn_hash.hex())
            return res