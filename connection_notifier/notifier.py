#!/usr/bin/env python3
import sys
import time
import os
import errno
from os import path

from datetime import datetime
import pyttsx3
from speedtest import ConfigRetrievalError, Speedtest as Spd
import matplotlib.pyplot as plt

from connection_notifier.configs import settings

# GLOBALS
EPSILON = 0.001  # a minute is ~0.016 hours, this is more than enough
SIXTY = 60.0
MEBI = 2 ** 20


# TODO add project to pypi: https://packaging.python.org/tutorials/packaging-projects/
# TODO: fix possible error where a minute might be skipped because of sleep + 2 speedtests (possible?)
# TODO: add maximum allowed spikes setting to ignore ~1 in 10 high pings/ low speeds

def get_speed_data(upload=False):
    try:
        spd = Spd()
    except ConfigRetrievalError as e:
        print("speedtest raised error:", e.message)
        print("skipping this time.")
        return
    print("testing download...")
    spd.download()
    if upload:
        print("testing upload...")
        spd.upload()
    res = spd.results.dict()
    assert res, "no results from speedtest"
    res['ping'] = int(res['ping'])
    print('ping =', res['ping'])
    res['download'] = int(res['download'] / MEBI)
    print('download =', res['download'])
    if upload:
        res['upload'] = int(res['upload'] / MEBI)
        print('upload =', res['upload'])
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
    print("voice selected:", random_voice)
    e.setProperty('voice', random_voice)


def say_something(e, msg, hour=0, force=False):
    if force or settings['hour_start'] < hour < settings['hour_end']:
        e.say(msg)
        e.runAndWait()


def download_and_plot():
    """
    measure ping 5 times and graph it
    :return:
    """
    print("checking ping")
    x = []
    y = []
    for i in range(5):
        print("iteration", i)
        y.append(get_speed_data()['ping'])
        x.append(datetime.now())
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.show()


def set_voice(e):
    target = settings['voice']
    voices = e.getProperty('voices')
    if target == 'random':
        set_random_voice(e)
        return

    for v in voices:
        if target.lower() in v.id.lower():
            selected = v.id
            break
    else:  # no match, don't change voice
        return
    # match found, change voice
    e.setProperty('voice', selected)


def evenly_divisible(a, b):
    return abs(a % b) < EPSILON or abs(b - a % b) < EPSILON


def plot_all_data(saved_download, saved_upload, saved_ping, now):
    # plot speed
    plt.subplot(311)
    plt.xlabel("date")
    plt.ylabel("megabytes")
    plt.plot(saved_download['x'], saved_download['y'])
    if settings['check_upload']:
        plt.plot(saved_upload['x'], saved_upload['y'])
        plt.legend(["download", "upload"])
    else:
        plt.legend(["download"])
    plt.gcf().autofmt_xdate()
    plt.title("speed")

    # plot ping
    plt.subplot(313)
    plt.xlabel("date")
    plt.ylabel("millisec")
    plt.plot(saved_ping['x'], saved_ping['y'], 'g')
    plt.gcf().autofmt_xdate()
    plt.title("ping")

    # save plot
    destination_dir = path.join(settings['plot_directory'], "plots")
    destination_file = path.join(destination_dir, "plot" + "-" + now.strftime("%Y-%m-%d-%H-%M"))
    try:  # make directories, ignore exception if they already exist
        os.makedirs(destination_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print("saving to", path.abspath(destination_file))
    plt.savefig(destination_file)
    plt.close()


def main_loop():
    """
    starts infinite loop which periodically uses speedtest and notifies if the output is not within the defined bounds.
    :return:
    """
    print("starting main loop")
    e = pyttsx3.init()
    set_voice(e)
    say_something(e, "hello world", force=True)
    saved_ping = {'x': [], 'y': []}
    saved_download = {'x': [], 'y': []}
    saved_upload = {'x': [], 'y': []}
    store_next_speedtest = False
    while True:
        try:
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:  # new day
                set_voice(e)

            if evenly_divisible(now.hour + now.minute / SIXTY, settings['graph_save_interval']):
                plot_all_data(saved_download, saved_upload, saved_ping, now)

                # clear dictionaries
                saved_ping, saved_download, saved_upload = {'x': [], 'y': []}, {'x': [], 'y': []}, {'x': [], 'y': []}

            # store next speedtest data
            if evenly_divisible(now.hour + now.minute / SIXTY, settings['graph_add_interval']):
                store_next_speedtest = True

            if evenly_divisible(now.minute, settings['download_interval']):
                print(now.strftime("%Y-%m-%d, %H:%M") + ": starting speedtest")
                data = get_speed_data(upload=settings['check_upload'])
                if data:
                    if data['ping'] > settings['ping_upper_limit']:
                        msg = "BAD PING! %d milli seconds." % data['ping']
                        say_something(e, msg, now.hour)
                    if data['download'] < settings['download_lower_limit']:
                        msg = "BAD DOWNLOAD SPEED! %d megabits per second." % data['download']  # it's actually mebibits
                        print(f"download < {settings['download_lower_limit']}")
                        say_something(e, msg, now.hour)
                    if settings['check_upload'] and data['upload'] < settings['upload_lower_limit']:
                        msg = "BAD UPLOAD SPEED! %d megabits per second." % data['upload']
                        print(f"upload < {settings['upload_lower_limit']}")
                        say_something(e, msg, now.hour)
                    if store_next_speedtest:
                        saved_ping['x'].append(now)
                        saved_ping['y'].append(data['ping'])
                        saved_download['x'].append(now)
                        saved_download['y'].append(data['download'])
                        if settings['check_upload']:
                            saved_upload['x'].append(now)
                            saved_upload['y'].append(data['upload'])
                        store_next_speedtest = False
                # wait either way
                time.sleep(60)
            else:
                time.sleep(30)
        except:
            say_something(e, settings['last_words'], datetime.now().hour)
            raise


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == '-p':
        download_and_plot()
    else:
        main_loop()
