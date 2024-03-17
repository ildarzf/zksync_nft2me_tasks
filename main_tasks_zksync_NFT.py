import random
import sys
import sqlite3
from web3 import Web3
from loguru import logger
import time

from config import ACCOUNTS, PROXIES
from utils.get_proxy import check_proxy
from utils.sleeping import sleep
from settings import USE_PROXY, RANDOM_WALLET, IS_SLEEP, SLEEP_FROM, SLEEP_TO
from modules_settings import *


file_path = "completed_tasks.db"
rpc_eth = "https://rpc.ankr.com/eth"
# Создайте подключение к базе данных
conn = sqlite3.connect('completed_tasks.db')
cursor = conn.cursor()

# Создайте таблицу для хранения выполненных задач, включая столбцы ethereum_address и task_description
cursor.execute('''CREATE TABLE IF NOT EXISTS completed_tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_description TEXT,
                    ethereum_address TEXT
                 )''')


tasks = [
        "1-NFT on NFTS2ME-FONT",
        "2-NFT on NFTS2ME-ENERGY",
        "3-NFT on NFTS2ME-MIRAGE",
        "4-NFT on NFTS2ME-GALACT",
        "5-NFT on NFTS2ME-ZEPHYR",
        "6-NFT on NFTS2ME-QUANTUM",
        "7-NFT on NFTS2ME-ARCAN",
        "8-NFT on NFTS2ME-IMPULSE",
        "9-NFT on NFTS2ME-VORTEX",
        "10-NFT on NFTS2ME-SIREN",
        "11-NFT on NFTS2ME-ORACLE",
        "12-NFT on NFTS2ME-SPARKLE",
        "13-NFT on NFTS2ME-PIE",
        "14-NFT on NFTS2ME-OWL",
        "15-NFT on NFTS2ME-ZENITH",
        "16-NFT on NFTS2ME-SPHERE",
        "17-NFT on NFTS2ME-DRAGON",
        "18-NFT on NFTS2ME-CITADEL",
        "19-NFT on NFTS2ME-ECLIPSE",
        "20-NFT on NFTS2ME-DNA",
        "21-NFT on NFTS2ME-Bitcoin",
        "22-NFT on NFTS2ME-DefiPepe",
        "23-NFT on NFTS2ME-Holidays",
        "24-NFT on NFTS2ME-15GWEI"
    ]

def execute_random_task(ethereum_address, cursor, conn, try_again):
    unfinished_tasks = [task for task in tasks if task not in get_completed_tasks(ethereum_address, cursor)]
    print('Выполненные задания:', get_completed_tasks(ethereum_address, cursor))
    print('Осталось сделать: ', unfinished_tasks)
    web3 = Web3(Web3.HTTPProvider(rpc_eth))
    account = web3.eth.account.from_key(ethereum_address)
    proxy = random.choice(PROXIES)
    address = account.address
    account_id = 1
    key = ethereum_address
    if unfinished_tasks:
        rand = 1 #random.choice([0, 1])
        if rand == 1:
            task_to_execute = random.choice(unfinished_tasks)
            print(f"Адрес ZKsync {address}: Выполнение задачи: {task_to_execute}")
            if task_to_execute == "1-NFT on NFTS2ME-FONT":
                module = mint_nft
                contracts = ["0x78A900067c7F634105a9be711aB338AF8068C686"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "2-NFT on NFTS2ME-ENERGY":
                module = mint_nft
                contracts = ["0x8a6f12Db092Cc0D0D7D4a10cfCc803B05399D0a8"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "3-NFT on NFTS2ME-MIRAGE":
                module = mint_nft
                contracts = ["0x148D0f93bE11f780166345d85626474D2230aEa4"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "4-NFT on NFTS2ME-GALACT":
                module = mint_nft
                contracts = ["0x84741ad693fd845720BD86da9E23e47fC305095f"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "5-NFT on NFTS2ME-ZEPHYR":
                module = mint_nft
                contracts = ["0x6F361FC86296C3C2C723BBE3B1Cce2C1296841A1"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "6-NFT on NFTS2ME-QUANTUM":
                module = mint_nft
                contracts = ["0x684626f35eF51e20Ac222179A0e98AB363bE8182"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "7-NFT on NFTS2ME-ARCAN":
                module = mint_nft
                contracts = ["0xBE61F663FbBd2d5b59587A96A2E9728F521FC692"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "8-NFT on NFTS2ME-IMPULSE":
                module = mint_nft
                contracts = ["0xd3595015f6747f21364FC762e1Cfd3Bb2007B4dD"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "9-NFT on NFTS2ME-VORTEX":
                module = mint_nft
                contracts = ["0x109f3916985f04729eF1c1a581F044a7E38Dd0D1"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "10-NFT on NFTS2ME-SIREN":
                module = mint_nft
                contracts = ["0x3FCcEb9ce767ee08afC0b1b034A07ccf3168737A"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "11-NFT on NFTS2ME-ORACLE":
                module = mint_nft
                contracts = ["0x96fC1eA93c3486891896FBa93a91cE32898aD3fD"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "12-NFT on NFTS2ME-SPARKLE":
                module = mint_nft
                contracts = ["0xd348697306875b44223F77122B7BC73A496cd495"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "13-NFT on NFTS2ME-PIE":
                module = mint_nft
                contracts = ["0x051601037A92353f840eBa76dea95FCb59C1717F"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "14-NFT on NFTS2ME-OWL":
                module = mint_nft
                contracts = ["0x53541Cc5D004265fbacD8e2AFD09ca4eE38F66AD"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "15-NFT on NFTS2ME-ZENITH":
                module = mint_nft
                contracts = ["0xA83F0e2A89f7aB7ac7cD7712e3A8271353E53DEf"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "16-NFT on NFTS2ME-SPHERE":
                module = mint_nft
                contracts = ["0x47faA52c4dcf6B779479Ac295C26875f656Ba4fe"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "17-NFT on NFTS2ME-DRAGON":
                module = mint_nft
                contracts = ["0xB166cfc6f3474Da7Aa76d94C83B2CaC3dA256e2d"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "18-NFT on NFTS2ME-CITADEL":
                module = mint_nft
                contracts = ["0xEF6740E485E423C5E6c349BF63E8F4d7221F77C2"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "19-NFT on NFTS2ME-ECLIPSE":
                module = mint_nft
                contracts = ["0x312182CEBb813EcF88cB194105ccBa1de2658B3f"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "20-NFT on NFTS2ME-DNA":
                module = mint_nft
                contracts = ["0x958F00CE381EaB69C76312cDF89A083d4309a1e1"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "21-NFT on NFTS2ME-Bitcoin":
                module = mint_nft
                contracts = ["0x3d814F24Ab9D12b9d5d24F1963227a1F7CaB9109"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "22-NFT on NFTS2ME-DefiPepe":
                module = mint_nft
                contracts = ["0x43Ab7465c802Ea8c74AB8C5C5F04F952D4860f53"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "23-NFT on NFTS2ME-Holidays":
                module = mint_nft
                contracts = ["0xB4cd3F3995dB72c1E8AadFaF12f3c0808f255CeE"]
                res = run_module(module, account_id, key, proxy, contracts)
            if task_to_execute == "24-NFT on NFTS2ME-15GWEI":
                module = mint_nft
                contracts = ["0x4e5b5B21743E0d24A96DBE446153Beb2E35F1b70"]
                res = run_module(module, account_id, key, proxy, contracts)
            
            if 'True' in str(res):
                mark_task_as_completed(task_to_execute, ethereum_address, cursor, conn)
            else:
                if try_again < 1: # кол-во попыток повторного запуска при ошибке
                    try_again += 1
                    logger.warning(f'Не получилось выполнить {task_to_execute}. Пробую сделать другое задание')
                    execute_random_task(ethereum_address, cursor, conn, try_again)
                else:
                    logger.warning('Не получилось выполнить. Попробую при следующем запуске')
            tm = random.randint(SLEEP_FROM, SLEEP_TO)
            logger.info(f'Пауза {tm}')
            time.sleep(tm)  # задержка
            #mark_task_as_completed(task_to_execute, ethereum_address, cursor, conn)
        else:
            print(f"Кошелек Ethereum {ethereum_address}: Пропущен сегодня!")
    else:
        print(f"Кошелек Ethereum {ethereum_address}: Все задачи выполнены!")

# Получение списка выполненных задач из базы данных для конкретного кошелька Ethereum
def get_completed_tasks(ethereum_address, cursor):
    cursor.execute("SELECT task_description FROM completed_tasks WHERE ethereum_address = ?", (ethereum_address,))
    completed_tasks = [row[0] for row in cursor.fetchall()]
    return completed_tasks

# Пометить задачу как выполненную в базе данных для конкретного кошелька Ethereum
def mark_task_as_completed(task_description, ethereum_address, cursor, conn):
    cursor.execute("INSERT INTO completed_tasks (task_description, ethereum_address) VALUES (?, ?)", (task_description, ethereum_address))
    conn.commit()

# Функция для выполнения одной задачи для конкретного кошелька Ethereum
def execute_one_task_for_ethereum_address(ethereum_address, cursor, conn, try_again):
    execute_random_task(ethereum_address, cursor, conn, try_again)
    tm = random.randint(5, 10)
    logger.info(f'Пауза {tm}')
    time.sleep(tm)   # задержка




def execute_tasks_in_thread_pool(ethereum_addresses):
    num = 0
    print('Всего кошельков', len(ethereum_addresses))
    for ethereum_address in ethereum_addresses:
       try:
            num += 1
            print(num,'/',len(ethereum_addresses))
            try_again = 0
            conn = sqlite3.connect('completed_tasks.db')
            cursor = conn.cursor()
            execute_one_task_for_ethereum_address(ethereum_address, cursor, conn, try_again)
            conn.close()
       except Exception as err:
            print(err)


def answer():
    print('Что будем делать?')
    print('1 - Продолжить текущие задания.')
    print('2 - Удалить текущую базу данных и начать все задания с начала.')
    answer_usr = input('Введите свой ответ 1 или 2 и нажмите ENTER: ')
    if answer_usr == '1':
        print('Продолжаем работу')
    elif answer_usr == '2':
        cursor.execute("DELETE FROM completed_tasks")
        conn.commit()
    else:
        print('Такого ответа нет. Попробуйте еще раз.')
        answer()



# def get_wallets():
#     if USE_PROXY:
#         account_with_proxy = dict(zip(ACCOUNTS, PROXIES))
#
#         wallets = [
#             {
#                 "id": _id,
#                 "key": key,
#                 "proxy": account_with_proxy[key]
#             } for _id, key in enumerate(account_with_proxy, start=1)
#         ]
#     else:
#         wallets = [
#             {
#                 "id": _id,
#                 "key": key,
#                 "proxy": None
#             } for _id, key in enumerate(ACCOUNTS, start=1)
#         ]
#     return wallets


def run_module(module, account_id, key, proxy, contracts):
    res = module(account_id, key, proxy, contracts)
    return res

def main():

    answer()

    wallets = ACCOUNTS

    if RANDOM_WALLET:
        random.shuffle(wallets)

    execute_tasks_in_thread_pool(wallets)
    #
    # for account in wallets:
    #     if account["proxy"]:
    #         logger.info(f"Trying to connect to the proxy [{account['proxy']}]")
    #
    #         result = check_proxy(account["proxy"])
    #
    #         if result is False:
    #             logger.error(f"Proxy error - {account['proxy']}")
    #             continue
    #
    #         logger.success(f"Proxy [{account['proxy']}] is available")
    #
    #     run_module(module, account["id"], account["key"], account["proxy"])
    #
    #     if account != wallets[-1] and IS_SLEEP:
    #         sleep(SLEEP_FROM, SLEEP_TO)


if __name__ == '__main__':


    #
    # module = get_module()
    # if module == "tx_checker":
    #     get_tx_count()
    # else:
    main()


