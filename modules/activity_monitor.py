import discord
from sqlitedict import SqliteDict

class ActivityMonitor:

    CLASS_KEY = "ActivityHistory"

    def __init__(self, guild_members, dataManager):
        self.activityMonitorDataManager = dataManager
        self.activityMonitorDataManager.ensure_category(self.CLASS_KEY, {})

    def full_activity_check(self, guild_members): # Will be run every 5 minutes, so will assume user has been doing a given activity for that time.
        with SqliteDict("./data/memberData.db") as member_data:
            for member in guild_members:
                print(f"{member.display_name} is currently doing {member.activity}")
                if len(member.activities) != 0:
                    main_activity = member.activities[0] 
                    current_history = self.activityMonitorDataManager.get_data(member, self.CLASS_KEY) # Dictionary
                    if current_history == None:
                        return
                    if main_activity.name not in current_history.keys():
                        current_history[main_activity.name] = 5
                    else:
                        current_time = current_history[main_activity.name]
                        current_time += 5
                        current_history[main_activity.name] = current_time
        member_data.commit()
        
        self.activityMonitorDataManager.dump_database()
