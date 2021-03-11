class Stopwatch:    
        def __init__(self):
                self.start = 0.0

        def handler(self, task):
                msg = ""
                if task == "start a stopwatch": #start a stopwatch
                        def startWatch():
                                self.start = time.time()
                        msg = "\nStarted a stopwatch"
                        return msg, startWatch()
                elif task == "stop the stopwatch": #stop the stopwatch
                        if(self.start != 0):
                                stop = "{0:.2f}".format(time.time() - self.start)
                                self.start = 0
                                msg = "\nstopwatch ran for "+stop+" seconds"
                                return msg, None
                        else:
                                msg = "\nstopwatch was never started"
                                return msg, None
                else:
                        msg = task,"is not a known task"
                        return msg, None

def commands():
    comm = [
                ["start a stopwatch", "begin a stopwatch", "setup a stopwatch"],
                ["stop the stopwatch", "terminate the stopwatch", "end the stopwatch"]
            ]
    classify = [
            "cosine",
            "cosine"
            ]
    return comm, classify

def handler(sentence, watch):
    watch.handler(sentence)
