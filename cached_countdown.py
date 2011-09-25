from parse_countdown import Countdown
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'memory' # or 'file'
}
countdown_cache = CacheManager(**parse_cache_config_options(cache_opts))

class CachedCountdown(Countdown):

	def __init__(self):
		print "init cached countdown"

	@countdown_cache.cache('getCountdownJSON', expire=15)
	def getCountdownJSON(self, *stop_number):
		json_data = Countdown.getCountdownJSON(self, *stop_number)
		return json_data

if __name__ == '__main__':
	countdown = CachedCountdown()
	print countdown.getCountdownJSON(50980)

