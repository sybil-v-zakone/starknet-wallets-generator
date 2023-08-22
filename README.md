![sybilvzakonebg.png](images%2Fsybilvzakonebg.png)
# Starknet Wallet Generator

#### *Описание:*

Скрипт имеет 5 модулей:
1. `generate_wallets` создает **ArgentX** кошельки.
2. `deploy_wallets` деплоит ранее сгенерированные кошельки в сеть StarkNet. 
3. `generate_and_deploy_wallets` объединяет в себе генерацию и деплой кошельков.
4. `export_wallets` экспортирует данные о кошельках в **Excel** файлы. *(Экспортирует кошельки: сгенерированные, неуспешно задеплоенные, успешно задеплоенные)*.
0. `exit` завершает работу скрипта

#### *Установка:*

1. `cd путь/к/проекту`
2. `pip install -r requirements.txt`

#### *Настройка:*

Все настройки находятся в файле `config.py`

- `ENDLESS_MENU` Установите значение `True`, если вы хотите, чтобы после отработки выбранного модуля опять появлялось меню.
- `WALLETS_TO_GENERATE_COUNT` Количество генерируемых кошельков.
- `GENERATED_WALLETS_JSON_PATH` Путь для сохранения сгенерированных кошельков в формате JSON.
- `GENERATED_WALLETS_EXCEL_PATH` Путь для сохранения сгенерированных кошельков в формате Excel.
- `DEPLOY_SLEEP_DEVIATION_IN_SEC` Диапазон `(от, до)` времени задержки (в секундах) между деплоями.
- `DEPLOYED_WALLETS_TXT_PATH` Путь для сохранения адресов успешно задеплоенных кошельков в текстовом файле.
- `DEPLOYED_WALLETS_EXCEL_PATH` Путь для сохранения адресов успешно задеплоенных кошельков в формате Excel.
- `DEPLOY_FAILED_WALLETS_EXCEL_PATH` Путь для сохранения информации о неуспешно задеплоенных кошельках в формате Excel.
- `DEPLOY_FAILED_WALLETS_JSON_PATH` Путь для сохранения информации о неуспешно задеплоенных кошельках в формате JSON.
- `LOAD_OKX_API_CONFIG_FROM_ENV` Установите значение `True`, если хотите загрузить конфигурацию OKX API из файла `.env`.
- `OKX_API_CONFIG` Настройки конфигурации для OKX API, включая ключ API, секрет, пароль и ограничение скорости.
- `CEX_WITHDRAW_FEE` Значение комиссии за вывод `ETH` из OKX.
- `SHOULD_WITHDRAW_FOR_DEPLOY` Установите значение `True`, если вы выводить `ETH` с OKX на каждый кошелек при деплое.
- `WITHDRAW_FOR_DEPLOY_ETH_AMOUNT` Количество `ETH`, которое будет выводиться с OKX перед деплоем кошелька.
- `WAIT_FOR_TOPUP_FROM_CEX_IN_SEC` Время ожидания (в секундах) пополнения с CEX.
- `WAIT_FOR_TOPUP_FROM_CEX_ATTEMPTS` Количество попыток ожидания пополнения с CEX. Установите отрицательное значение для бесконечного числа попыток.
- `STARKNET_NETWORK` Сеть для подключения, разрешенные значения: `"testnet"`, `"testnet2"` или `"mainnet"`.
- `STARKNET_CHAIN_ID` ID сети в Starknet, разрешенные значения: `StarknetChainId.TESTNET`, `StarknetChainId.TESTNET2` или `StarknetChainId.MAINNET`.

#### *Запуск:*
Для запуска скрипта в консоль нужно написать: `python main.py`, после чего перед вами появится выбор модулей:
![1.png](images%2F1.png)