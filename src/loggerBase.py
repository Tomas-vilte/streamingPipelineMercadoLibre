import logging as log

log_file = '/home/tomi/streamingPipelineMercadoLibre/logs/capaDatos.log'
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                datefmt='%Y-%m-%d %H-%M-%S',
                handlers =[
                    log.FileHandler(log_file),
                    log.StreamHandler()
                ])

