import logging

def configureLogger(filelocation):
   logging.basicConfig(filename=filelocation, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                       level=logging.INFO)

   logger = logging.getLogger()

   # create console handler and set level to debug
   ch = logging.StreamHandler()
   ch.setLevel(logging.INFO)

   # create formatter
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

   # add formatter to ch
   ch.setFormatter(formatter)

   logging.info('Logging Begining')
