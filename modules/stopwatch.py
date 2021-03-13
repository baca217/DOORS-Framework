import time

class Stopwatch:    
        def __init__(self):
                self.start = 0.0

        def handler(self, task):
                msg = ""
                if task == "start a stopwatch": #start a stopwatch
                        def startWatch():
                                self.start = time.time()
                        msg = "started a stopwatch"
                        return msg, startWatch()
                elif task == "stop the stopwatch": #stop the stopwatch
                        if(self.start != 0):
                                stop = "{0:.2f}".format(time.time() - self.start)
                                self.start = 0
                                msg = "stopwatch ran for "+stop+" seconds"
                                return msg, None
                        else:
                                msg = "stopwatch was never started"
                                return msg, None
                else:
                        msg = task+" is not a known task"
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

def command_handler(sentence):
    print("please use stopwatch object instead")

def c_builder():
    watch = Stopwatch
    return watch
