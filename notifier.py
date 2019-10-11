#!/usr/bin/env python2
import sys
import time

from datetime import datetime
from pyttsx import Engine
from speedtest import Speedtest as Spd
import matplotlib.pyplot as plt

import connection_alerter.configs.settings

FAMOUS_LAST_WORDS = """AAAAAAAAA,
                Hey let's watch the rain as it's falling down.
                Is this the reeal life, is this just fantasy?
                THE SHIPPP, IS SINKING!
                Help! I need somebody! Help! Not just anybody!
                ERROR NUMBER 1337: Core systems have been damaged.
                I can't feel my face but I like it.
                Friends applaud, the comedy is finished.
                Wake me up! wake me up inside. I can't wake up! wake me up inside.
                Saave mee! call my name and save me from the dark."""


def get_speed_data(upload=False):
    spd = Spd()
    print "testing download..."
    spd.download()
    if upload:
        print "testing upload..."
        spd.upload()
    res = spd.results.dict()
    assert res
    res['ping'] //= 1
    print 'ping', res['ping']
    res['download'] //= 2 ** 20
    print 'download', res['download']
    if upload:
        res['upload'] //= 2 ** 20
        print 'upload', res['upload']
    return res


def set_random_voice(e):
    """
    pick some voice based on the day of the week
    :param e:
    :return:
    """
    voices = e.getProperty('voices')
    today = datetime.now().day
    random_voice = voices[today % len(voices)].id
    e.setProperty('voice', random_voice)


def say_something(e, msg):
    e.say(msg)
    e.runAndWait()


def download_and_plot():
    """
    measure download speed 5 times and graph it
    :return:
    """
    x = []
    y = []
    for i in range(5):
        print i
        y.append(get_speed_data()[0])
        x.append(datetime.now())
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.show()


def save_daily_speed():
    # TODO: save speed every 2 hours and graph it
    plt.savefig('chngeme.png')


def main_loop():
    print "starting main loop:"
    e = Engine()
    while True:
        try:
            if datetime.now().minute % 15 == 0:
                print "starting speedtest", datetime.now().strftime("%Y-%m-%D, %H:%M")
                # TODO: if speed below certain number or ping above certain number, say it.
                time.sleep(60)
        except:
            say_something(e, FAMOUS_LAST_WORDS)
            raise


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == '-p':
        download_and_plot()
    else:
        main_loop()
