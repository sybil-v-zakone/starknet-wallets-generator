![sybilvzakonebg.png](images%2Fsybilvzakonebg.png)
# Starknet Wallet Generator

#### *Описание:*

Скрипт имеет 4 модуля:
1. `generate_wallets` создает **ArgentX** кошельки
2. `deploy_wallets` деплоит ранее сгенерированные кошельки в сеть StarkNet
3. `export_wallets` экспортирует данные о кошельках в **Excel** файл *(создаст один файл с 3мя листами)*
0. `exit` завершает работу скрипта

#### *Установка:*

1. `cd путь/к/проекту`
2. `python -m venv venv`
3. 
   Windows: `.\venv\Scripts\activate`
   
   Linux/MacOS: `source venv/bin/activate`
4. `pip install -r requirements.txt`

#### *Настройка:*
Для Windows воспользуйтесь данной инструкцией:

https://sybil-v-zakone.notion.site/sybil-v-zakone/starknet-py-578a3b2fb96e49149a52b987cbbb8c73

Все настройки находятся в файле `config.py`

- `ENDLESS_MENU` установите значение `True`, если вы хотите, чтобы после отработки выбранного модуля опять появлялось меню
- `WALLETS_TO_GENERATE_COUNT` количество генерируемых кошельков
- `GENERATED_WALLETS_JSON_PATH` путь для сохранения сгенерированных кошельков в формате JSON
- `DEPLOYED_WALLETS_TXT_PATH` путь для сохранения адресов успешно задеплоенных кошельков в текстовом файле
- `DEPLOY_FAILED_WALLETS_JSON_PATH` путь для сохранения информации о неуспешно задеплоенных кошельках в формате JSON
- `WALLETS_EXCEL_PATH` путь для экспорта данных о кошельках в **Excel**
- `LOAD_OKX_API_CONFIG_FROM_ENV` установите значение `True`, если хотите загрузить конфигурацию OKX API из файла `.env`
- `OKX_API_CONFIG` настройки конфигурации для OKX API, включая ключ API, секрет, пароль и ограничение скорости
- `CEX_WITHDRAW_FEE` значение комиссии за вывод `ETH` из OKX
- `DEPLOY_SLEEP_DEVIATION_IN_SEC` Диапазон `(от, до)` времени задержки (в секундах) между деплоями
- `SHOULD_WITHDRAW_FOR_DEPLOY` установите значение `True`, если вы выводить `ETH` с OKX на каждый кошелек при деплое
- `WITHDRAW_FOR_DEPLOY_ETH_AMOUNT` диапазон `(от, до)` количества `ETH`, которое будет выводиться с OKX перед деплоем кошелька
- `WAIT_FOR_TOPUP_FROM_CEX_IN_SEC` время ожидания (в секундах) пополнения с CEX
- `WAIT_FOR_TOPUP_FROM_CEX_ATTEMPTS` количество попыток ожидания пополнения с CEX. Установите отрицательное значение для бесконечного числа попыток
- `STARKNET_NETWORK` сеть для подключения, разрешенные значения: `"testnet"`, `"testnet2"` или `"mainnet"`
- `STARKNET_CHAIN_ID` ID сети в Starknet, разрешенные значения: `StarknetChainId.TESTNET`, `StarknetChainId.TESTNET2` или `StarknetChainId.MAINNET`
- `CLIENT_ON_ERROR_TOTAL_TRIES` количество попыток повтора при ошибке клиента Starknet
- `CLIENT_ON_ERROR_SLEEP_IN_SEC` время ожидания перед следующей попыткой повтора после ошибки клиента Starknet
- `GAS_THRESHOLD` это переменная, которая задает пороговое значение стоимости газа в гигавей (GWEI). Если текущая стоимость газа превышает установленное значение `GAS_THRESHOLD`, то выполнение скрипта приостанавливается и ожидает, пока стоимость газа не уменьшится до уровня, допустимого порогового значения
- `GAS_DELAY_RANGE` это интервал времени в секундах между проверками стоимости газа. Программа периодически проверяет стоимость газа перед отправкой транзакций, чтобы определить, установлена ли она выше `GAS_THRESHOLD`. Интервал задержки позволяет программе ожидать, чтобы избежать частых запросов и нагрузки на сеть

#### *Запуск:*
1. Откройте командную строку или терминал
2. Перейдите в директорию, где находится файл `main.py`
3. Активируйте виртуальное окружение:
    
    Windows: `.\venv\Scripts\activate`
    
    Linux/MacOS: `source venv/bin/activate`
4. Запустите программу, выполнив следующую команду: `python main.py`
5. После запуска `main.py` перед вами появится выбор модулей:

![1.jpeg](images%2F1.jpeg)
