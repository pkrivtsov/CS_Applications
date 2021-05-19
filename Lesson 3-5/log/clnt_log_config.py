import logging
 
logging.basicConfig(
	filename = 'log/info.log',
	level = logging.INFO,
	format = '[%(asctime)-10s] %(levelname).1s %(module)s %(message)s',
	datefmt = '%Y.%m.%d %H:%M:%S',
)



