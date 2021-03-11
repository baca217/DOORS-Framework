def command_handler(sentence):
    if "set a timer for" in sentence:
        setTimer(sentence)

def commands():
    comm = [
            ["set a timer for"]
            ]
    classify = [
            "exact"
            ]
    return comm, classify

def handler(signal, frame): #handler for timer
        print("\n\nTime is up for timer!\n")

def setTimer(timeStr): #only going to focus on time for now
        temp = ""
        arr = timeStr.split()
        num = 0
        strNum = ""
        msg = ""
        timeSwitch = { #dictionary for scaling the time
            "second": 1,
            "minute": 60,
            "hour": 3600,
            }

        try:
                timeFormat = arr[-1].strip() #get time format
                arr = arr[:-1] #remove time format
        except: #failed to pull timeformat from string
                msg = "no time format was detected for setting a timer"
                return msg, None

        if(timeFormat[-1] is "s"): #removing trailing s. EX: seconds, minutes
                timeFormat = timeFormat[:-1]

        for f in range(len(arr),0,-1): #pulling time amount out of string
                try:
                        strtemp = " ".join(arr[f-1:]) #pull substring and see if it's a number          
                        numtemp = w2n.word_to_num(strtemp)
                        num = int(numtemp)
                except valueerror:
                        break

        if(timeFormat not in timeSwitch.keys()): #error 1: no time format
                msg = timeFormat+" is not a valid time format"
                return msg, None
        elif(num == 0): #error 2: time requested is 0 for timer
                msg = "can't set a timer for 0 "+timeFormat
                return msg, None

        msg = "\nsetting timer for "+str(num)+" "+timeFormat
        if num > 1:
                msg += "s"
        def setSignal():
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(num * timeSwitch[timeFormat])
        return msg, setSignal
