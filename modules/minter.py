import random
from typing import Union, List

from loguru import logger
from config import MINTER_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Minter(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

    def get_tx_data(self):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
        }
        return tx

    @retry
    @check_gas
    def mint_nft(self, contracts: List):
        logger.info(f"[{self.account_id}][{self.address}] Mint NFT on NFTS2ME")

        contract = self.get_contract(random.choice(contracts), MINTER_ABI)

        tx_data = self.get_tx_data()

        transaction = contract.functions.mint().build_transaction(tx_data)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        res = self.wait_until_tx_finished(txn_hash.hex())

        return res
