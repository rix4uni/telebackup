## telebackup

Scrape all posts in a telegram channel and saves to another channel.

## Installation
```
git clone https://github.com/rix4uni/telebackup.git
cd telebackup
python3 setup.py install
```

## pipx
Quick setup in isolated python environment using [pipx](https://pypa.github.io/pipx/)
```
pipx install --force git+https://github.com/rix4uni/telebackup.git
```

## Usage
```
telebackup
```

## Todo
- add a option that can check 100, 200 according to users need posts recently uploaded instead of cheking all message of a channel
- add a option that can check posts recently uploaded within 1day, 2day according to users need instead of cheking all message of a channel
- add a option to use multiple telegram session like telegram_1.session, telegram_2.session
- add dealy to avoid rate limit and resend those message not sent because of rate limited exceed