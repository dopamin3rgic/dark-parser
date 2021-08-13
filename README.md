# dark-parser
This tool can be used to parse HTML files from popular deep/dark web forums. This tool does **NOT** crawl the forums (there are plenty of tools that will already do this) and it assumes you have the relevant HTML files stored locally on your machine. It currently works with **forum threads** from RaidForums, Exploit.in, and Omerta. The output file can be used to more easily run analysis of the posts & posters on the forum. 

## Setup
Install BeautifulSoup if you don't have it already: `pip install bs4`

## Usage
Basic Syntax:
`python3 darkparser.py {forum} -d {filepath}`

```
user@host:~/dark-parser$ ./darkparser.py -h
usage: darkparser.py [-h] {raidforums,exploitin,omerta} ...

Parses threads, posts, dates, and usernames from deep/dark web forums.

positional arguments:
  {raidforums,exploitin,omerta}

optional arguments:
  -h, --help            show this help message and exit
user@host:~/dark-parser$ ./darkparser.py raidforums -h
usage: darkparser.py raidforums [-h] [-o <filename>] -d <filepath>

Parses HTML files from RaidForums

optional arguments:
  -h, --help            show this help message and exit
  -o <filename>, --output <filename>
                        Name of the output file (CSV)
  -d <filepath>, --directory <filepath>
                        Path to directory where HTML files are located

```

## Examples

### Using -o option
```
user@host:~/dark-parser$ python3 darkparser.py raidforums -d ./rf_htmls -o rf_threads.csv
Parsing Thread: $0.5 NordVPN ACCOUNTS [ WARRANTY ]
Parsing Thread: 0.005$ Minecraft accounts
Parsing Thread: [#0] SUPER EARNINGS | EXCELLENT MIX OF WHITEHAT & BLACKHAT METHODS | EARN $200 DAILY
Parsing Thread: 000webhost.com 14.8kk
Parsing Thread: $0.03 each | Discord Tokens [VERIFIED] Checked Daily
Parsing Thread: 0 S C P - Exam writeup (x8) $150

Done processing 24 posts!
Writing posts to rf_threads.csv
```
### Standard mode
```
user@host:~/dark-parser$ python3 darkparser.py omerta -d ./omerta-htmls/
Parsing Thread: Anonymous Worldwide VPN Service
Parsing Thread: Прогон 7ым XRumerоm по форумам  блогам  гостевым. ru и en базы
Parsing Thread: WWW.FE-ACC18.RU!!!!! SellCC + CVV !!!!!! Легендарный сервис по продаже СС !!!!!!!!!
Parsing Thread: BEST CC  DL  BILLS TEMPLATE SERVICE
Parsing Thread: Selling DIEBOLD OPTEVA SKIMMER- ( Complete With Camkit -- (Ready to Work)
Parsing Thread: MKL Keylogger серия: 2015
Parsing Thread: Международный телефонный/SMS биллинг!
Parsing Thread: [SSNDOB.RU] SSN/auto-manual/FULLS/DL/CR&BR -best prices!!! [SSNDOB.RU]
Parsing Thread: Elite VPN Service ver.3 - Quad VPN  Double VPN  Dynamic IP  Port Forwarding
Parsing Thread: Unique Best CC&DUMPS Shop
Parsing Thread: VPN-Service/Best OPENVPN GUI/Double VPN
Parsing Thread: Mr.Perfect's DMV Quality ENHANCED Driver License 20+ States + We Sell Credit Report & SSN DOB (100% Faster Sevice and)
Parsing Thread: ??? Darkness (Optima) DDoS Bot Поколение XX
Parsing Thread: SSN DOB  MMN  MDOB  DL lookups  Credit profiles!
Parsing Thread: APPROVED.XXX-ONLINE SHOP CC+CVV/SSN+DOB/CHECKER/MMN/PAYPAL

Done processing 150 posts!
Writing posts to omerta.csv
```
## Future Development
- More forum options to come.
- Exception handling for when non-thread files or when incorrect forum files are passed to `-d `
