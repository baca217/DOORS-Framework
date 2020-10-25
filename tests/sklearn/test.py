import local_commands as loc
import time

def test_watch():
    watch = loc.Stopwatch()
    watch = loc.check_command("homie start a stopwatch", watch)
    time.sleep(6)
    watch = loc.check_command("homie stop the stopwatch", watch)

def test_weather():
    loc.check_command("homie what's the weather like", "homie what's the weather like")

def test_music(sn):
    loc.check_command("homie play the song", "homie play the song "+sn)

def test_reminder():
    loc.check_command("homie set a reminder", "homie set a reminder for 5 seconds")
    time.sleep(6)

def main():
    #test_watch()
    #test_weather()
    #test_music("Impact Mode")
    test_reminder()

if __name__ == "__main__":
    main()
