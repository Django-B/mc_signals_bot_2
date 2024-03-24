from loguru import logger

logger.add('debug.log', format='{time} | {level} | {name}:{function}:{line} | {message}', level='DEBUG', retention='1 day')
