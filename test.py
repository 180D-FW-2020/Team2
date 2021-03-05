from Stats.stats import *
from Mood_Tracker.mood_tracker_spotify_gen import *

user_stat = userStats()
user_stat.user_id = 'jackielam'

my_moods = moodTracker()
my_moods.run_task()

print(my_moods.mood_list, my_moods.song_dict)
user_stat.addMood(my_moods.mood_list, my_moods.song_dict)

