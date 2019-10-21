FAMOUS_LAST_WORDS = """AAAAAAAAA,
                Hey let's watch the rain as it's falling down.
                Is this the reeal life, is this just fantasy?
                THE SHIPPP IS SINKING!
                Help! I need somebody! Help! Not just anybody!
                ERROR NUMBER 1337: Core systems have been damaged.
                I can't feel my face but I like it.
                Friends applaud, the comedy is finished.
                Wake me up! wake me up inside. I can't wake up! wake me up inside.
                Save mee! call my name and save me from the dark."""

# these are settings you can change as you'd like, don't mess up the types.
settings = {
    'voice': "random",  # (STRING) random, hazel, david, or zira
    'plot_directory': ".",  # (STRING) this is where the graph PNGs will be saved
    'graph_save_interval': 1.5,  # (HOURS) how often a graph will be saved and data reset
    'graph_add_interval': 0.1,  # (HOURS) how often data will be added - can't be less than download_interval
    'download_interval': 15,  # (MINUTES) how often a speedtest will be run
    'download_lower_limit': 30,  # (MEGABYTES) speed lower than this will be notified
    'ping_upper_limit': 150,  # (MILLISEC) ping higher than this will be notified
    'upload_lower_limit': 1,  # (MEGABYTES) speed lower than this will be notified
    'check_upload': True,  # True/False - decide whether to check+save upload speed
    'last_words': FAMOUS_LAST_WORDS,  # what to say if program crashes
    'hour_start': 8,  # (HOURS) before this time, nothing will be said. 0 for no limit
    'hour_end': 20,  # (HOURS) after this time, nothing will be said. 24 for no limit
}
