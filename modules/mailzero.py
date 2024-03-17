import random
from typing import Union

from loguru import logger
from config import MAILZERO_ABI, MAILZERO_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class MailZero(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(MAILZERO_CONTRACT, MAILZERO_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    @retry
    @check_gas
    def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint MailZero NFT")

        transaction = self.contract.functions.mint(196264).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        res = self.wait_until_tx_finished(txn_hash.hex())
        return res