
API_BASE_URL = 'https://min-api.cryptocompare.com/'
DATA_URL = API_BASE_URL + 'data/'
DATA_V2_URL = DATA_URL + 'v2/'
DATA_V3_URL = DATA_URL + 'v3/'
DATA_V3_ALL_URL = DATA_V3_URL + 'all/'

# Specific APIs

# History APIs
DAILY_HISTORY_URL = DATA_V2_URL + 'histoday'
HOURLY_HISTORY_URL = DATA_V2_URL + 'histohour'
MINUTE_HISTORY_URL = DATA_V2_URL + 'minute'

# All the Coins API
COIN_LIST_URL = DATA_URL + 'all/coinlist'

# Social API
SOCIAL_BASE_URL = DATA_URL + 'social/coin/'
SOCIAL_LATEST_URL = SOCIAL_BASE_URL + 'latest'
SOCIAL_HISTORY_BASE_URL = SOCIAL_BASE_URL + 'histo/'
DAILY_SOCIAL_URL = SOCIAL_HISTORY_BASE_URL + 'day'
HOURLY_SOCIAL_URL = SOCIAL_HISTORY_BASE_URL + 'hour'

# Exchange symbols API
ALL_EXCHANGE_URL = DATA_V3_ALL_URL + 'exchanges'

# Exchange General Info API
EXCHANGE_INFO_URL = DATA_URL + 'exchanges/general'

# Blockchain API
BLOCKCHAIN_BASE_URL = DATA_URL + 'blockchain/'
BLOCKCHAIN_AVAILABLE_COINS_URL = BLOCKCHAIN_BASE_URL + 'list'
BLOCKCHAIN_HISTORICAL_DAILY_URL = BLOCKCHAIN_BASE_URL + 'histo/day'

# News API
NEWS_URL = DATA_V2_URL + 'news/'
