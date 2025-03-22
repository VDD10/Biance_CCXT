import ccxt
import sys
import json
from decimal import Decimal, getcontext
json_file_path = 'Link lead to yourfile.json'      

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
specific_data = data['enter your variable in //yourfile.json'] #Your_ApiKey
specific_data1 = data['enter your variable in //yourfile.json'] #Your-SecretApiKey
       
api_key = specific_data
api_secret = specific_data1

exchange = ccxt.binance({
'apiKey': api_key,
'secret': api_secret,
'enableRateLimit': True,
})

balance = exchange.fetch_balance()
usdt_balance = balance['total'].get('USDT', 0)
print(f"Số Dư USDT Hiện Tại Là: {usdt_balance} USDT")
usdc_balance = balance['total'].get('USDC', 0)
print(f"Số Dư USDC Hiện Tại Là: {usdc_balance} USDC")
free_balance = balance['free']

print("Số Coin Bạn Hiện Đang Nắm Giữ Ở Ví Spot Là:" "\n")
getcontext().prec = 50

for coin, amount in free_balance.items():
 amountDE = Decimal(amount)
 amountDEC = f"{amountDE:.10f}".rstrip('0').rstrip('.') if '.' in f"{amountDE:.10f}" else f"{amountDE:.10f}"
 if amount > 0:
  print(f"{coin}:{amountDEC}")

print("\n")
coinwant = input("Vui Lòng Chọn Coin Bạn Muốn Mua Hoặc Bán:" "\n")
coinwantup = coinwant.upper()
coinwant_balance = balance['free'].get(coinwantup, 0)
getcontext().prec = 50
coinwant_balanceDE = Decimal(coinwant_balance)
coinwant_balanceDEC= f"{coinwant_balanceDE:.10f}".rstrip('0').rstrip('.') if '.' in f"{coinwant_balanceDE:.10f}" else f"{coinwant_balanceDE:.10f}"

if coinwantup not in balance['free']:
 print("Không Tìm Thấy Coin Bạn Đã Chọn!")
 sys.exit()
else:
 sys.stdout.write("\033[F\033[K")
 sys.stdout.write("\033[F\033[K")  
 tradingpair = input("Vui Lòng Chọn Cặp Giao Dịch!" "\n" "Điền Vào Ô Cặp Giao Dịch Bạn Muốn(USDT, USDC):" "\n")
 tradingpairup = tradingpair.upper()
 if tradingpairup not in balance['free']:
  print("Không Tìm Thấy Cặp Giao Dịch Bạn Đã Chọn!")
  sys.exit()
 else:
  sys.stdout.write("\033[F\033[K")
  sys.stdout.write("\033[F\033[K")
  sys.stdout.write("\033[F\033[K") 
  symbol = f'{coinwantup}/{tradingpairup}'
  ticket = exchange.fetch_ticker(symbol)
  price = ticket['last']
  coinusd_balance = coinwant_balance * price
  usd_balance = balance['total'].get(tradingpairup, 0)
 
print(f"Số Dư Của Coin {coinwantup} Bạn Chọn Là: {coinwant_balanceDEC} Tương Đương Với {coinusd_balance} {tradingpairup}")
a = input("Bạn Muốn Mua Hay Bán?" "\n"
"Nhập 1 = Mua, Nhập 2 = Bán\n")
sys.stdout.write("\033[F\033[K")
sys.stdout.write("\033[F\033[K") 
sys.stdout.write("\033[F\033[K")
try:

    if a == '1':
      symbol = f'{coinwantup}/{tradingpairup}'
      ticket = exchange.fetch_ticker(symbol)
      price = ticket['last']
      getcontext().prec = 50
      priceDE = Decimal(price)
      priceDEC = f"{price:.10f}".rstrip('0').rstrip('.') if '.' in f"{price:.10f}" else f"{price:.10f}"
      print(f"Giá Hiện Tại Là {priceDEC} / 1 {coinwantup}")

      b = input("Bạn Muốn Mua Bao Nhiêu? (Vui Lòng Nhập Số Tiền, Đơn vị: USD)"
      "\n")
      usd_amount = float(b)
      sys.stdout.write("\033[F\033[K")
      sys.stdout.write("\033[F\033[K")
      if usd_balance < usd_amount:
       print("Không Thể Mua Do Số Tiền Mua Vượt Quá Số Tiền Hiện Có!")
      else:
       amount = usd_amount / price
       order = exchange.create_market_buy_order(symbol, amount)
       print(f"Bạn Đã Mua {amount} {coinwantup} Tương Đương Với Số Tiền Là {usd_amount} {tradingpairup} Thành Công!") 

    elif a == '2':
         symbol = f'{coinwantup}/{tradingpairup}'
         ticket = exchange.fetch_ticker(symbol)
         price = ticket['last']
         getcontext().prec = 50
         priceDE1 = Decimal(price)
         priceDEC1= f"{priceDE1:.10f}".rstrip('0').rstrip('.') if '.' in f"{priceDE1:.10f}" else f"{priceDE1:.10f}"
         print(f"Giá Hiện Tại Là {priceDEC1} / 1 {coinwantup}")

         b1 = input("Bạn Muốn Bán Bao Nhiêu? (Vui Lòng Nhập Số Tiền, Đơn vị: USD)"
      "\n")
         usd_amount1 = float(b1) 
         sys.stdout.write("\033[F\033[K")
         sys.stdout.write("\033[F\033[K")
         if coinusd_balance < usd_amount1:
          print(f"Không Thể Bán Do Số Tiền Bán Vượt Quá Số Coin {coinwantup} Đang Hiện Có!")
         else:
          amount1 = usd_amount1 / price
          order = exchange.create_market_sell_order(symbol, amount1)
          print(f"Bạn Đã Bán {amount1} {coinwantup} Tương Đương Với Số Tiền Là {usd_amount1} {tradingpairup} Thành Công!")

    else:
     print("Không Thể Đáp Ứng Yêu Cầu Do Nhập Sai Số!")

except ccxt.ExchangeError as e:
    print("Không Thể Đặt Lệnh Do Lỗi Từ Sàn!")
except ccxt.NetworkError as e:
    print("Xảy Ra Lỗi Do Không Có Mạng!")
