import random
from typing import Union
import time
from loguru import logger
from web3 import Web3
from config import L2TELEGRAPH_MESSAGE_CONTRACT, L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_MESSAGE_ABI, L2TELEGRAPH_NFT_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account
import requests


class L2Telegraph(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
        }

    def get_estimate_fee(self, contract_address: str, abi: dict):
        contract = self.get_contract(contract_address, abi)
        fee = contract.functions.estimateFees(
            175,
            self.address,
            "0x",
            False,
            "0x"
        ).call()
        return int(fee[0] * 1.2)

    def get_nft_id(self, txn_hash: str):
        receipts = self.w3.eth.get_transaction_receipt(txn_hash)

        nft_id = int(receipts["logs"][2]["topics"][-1].hex(), 0)

        return nft_id

    @retry
    @check_gas


    def create_msg(self):
        n = random.randint(1, 2)
        string = []
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        try:
           response = requests.get(word_site)
           if response.status_code == 200:
              for i in range(n):
                   WORDS = [g for g in response.text.split()]
                   string.append(random.choice(WORDS))
              msg = ' '.join(string)
              return msg
        except Exception as e:
            time.sleep(1)
            logger.info(f'Ошибка генерации сообщения. Пробую снова')
            return self.create_msg()

    def send_message(self):
        logger.info(f"[{self.account_id}][{self.address}] Send message")

        l0_fee = self.get_estimate_fee(L2TELEGRAPH_MESSAGE_CONTRACT, L2TELEGRAPH_MESSAGE_ABI)

        self.tx.update({"value": Web3.to_wei(0.00025, "ether") + l0_fee})

        contract = self.get_contract(L2TELEGRAPH_MESSAGE_CONTRACT, L2TELEGRAPH_MESSAGE_ABI)

        msg = self.create_msg()
        transaction = contract.functions.sendMessage(
            msg,
            175,
            "0x5f26ea1e4d47071a4d9a2c2611c2ae0665d64b6d0d4a6d5964f3b618d8e46bcfbf2792b0d769fbda"
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        res = self.wait_until_tx_finished(txn_hash.hex())
        return res

    def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint NFT")

        self.tx.update({"value": Web3.to_wei(0.0005, "ether")})

        contract = self.get_contract(L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_NFT_ABI)

        transaction = contract.functions.mint().build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        nft_id = self.get_nft_id(txn_hash.hex())
        return nft_id

    @retry
    @check_gas
    def bridge(self, sleep_from, sleep_to):
        l0_fee = self.get_estimate_fee(L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_NFT_ABI)

        nft_id = self.mint()

        sleep(sleep_from, sleep_to)

        self.tx.update({"value": l0_fee})
        self.tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        logger.info(f"[{self.account_id}][{self.address}] Bridge NFT [{nft_id}]")

        contract = self.get_contract(L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_NFT_ABI)

        transaction = contract.functions.crossChain(
            175,
            "0x5b10ae182c297ec76fe6fe0e3da7c4797cede02dd43a183c97db9174962607a8b6552ce320eac5aa",
            nft_id
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        res = self.wait_until_tx_finished(txn_hash.hex())
        return res