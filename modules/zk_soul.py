import random
from typing import Union

from loguru import logger
from config import ZKSOUL_CONTRACT, ZKSOUL_ABI, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class ZkSoulId(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(ZKSOUL_CONTRACT, ZKSOUL_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def get_random_name(self):
        domain_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        logger.info(f"[{self.account_id}][{self.address}] Mint {domain_name}.zksoul ID")

        return domain_name

    @retry
    @check_gas
    def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint zkSoul ID")

        domain_name = self.get_random_name()

        transaction = self.contract.functions.mint(
            domain_name,
            self.address,
            ZERO_ADDRESS
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        res = self.wait_until_tx_finished(txn_hash.hex())
        return res