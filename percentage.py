import os
import json
import scipy.stats as ss

# Load the statistics data from a json file
basedir = os.path.abspath(os.path.dirname(__file__))
with open("{}/{}".format(basedir, "total_stats.json"), "r") as f:
    total_info=json.load(f)

"""
{
    "height": {
        "statistic_info": {
            "male":{
                "19~24세": {
                    "average":174.4,
                    "std":5.75
                },
                ...
            },
            "female":{
                ...
            }
        }
    }
}
"""

# Define a class to calculate the percentile based on the user's physical information and the statistics data
class GetPercentage:
    def __init__(self, category):
        self.info=total_info[category]
        self.category=category

    # Get the age ranges for a specific gender
    def get_age_range(self, gender):
        return list(self.info["statistic_info"][gender].keys())

    # Get the source of the statistics data
    def get_source(self):
        return self.info["source"]

    # Calculate the percentile
    def get_percentage(self, age_range, gender, value):
        m=self.info["statistic_info"][gender][age_range]['average']
        s=self.info["statistic_info"][gender][age_range]['std']
        dif=ss.norm.cdf((value-m)/s)
        if self.category in ["height"]:
            return round(1-dif, 3)
        else:
            print(self.category,round(dif, 3), flush=True)
            return round(dif, 3)