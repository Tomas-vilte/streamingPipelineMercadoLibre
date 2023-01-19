import logging as log

log_file = '/home/tomi/streaming_pipeline/logs/capaDatos.log'
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                datefmt='%Y-%m-%d',
                handlers =[
                    log.FileHandler(log_file),
                    log.StreamHandler()
                ])

