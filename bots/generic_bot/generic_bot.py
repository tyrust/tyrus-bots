import time

'''
generic_bot.py

An generic bot class. I don't really know how this should work, but 
I am making this thing so that when I figure it out, I can just change
this backend without breaking whatever other stuff I do.
'''

class GenericBot:
    def __init__(self, runnable, interval=120):
        '''
        Keyword arguments:
        runnable -- function that the bot will perform every interval
        interval -- time in seconds that bot should perform function
        '''
        self.runnable = runnable
        self.interval = interval

    def run(self):
        while True:
            self.runnable()
            time.sleep(self.interval)

            

        
