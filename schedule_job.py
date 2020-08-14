import requests
import sys


class ScrapyCloudJob:

    def __init__(self, job_type='full'):
        self.job_type = job_type

    def run(self):
        return requests.post("https://app.scrapinghub.com/api/run.json?apikey=2018d259ee75404f93ad43dd8f236dbb",
                             data={"project": 468564, "spider": 'real_estate', "job_settings": {"JOB_TYPE": self.job_type}})


if __name__ == "__main__":
    if (len(sys.argv <= 1):
        response=ScrapyCloudJob().run()
    else:
        response=ScrapyCloudJob(job_type=sys.argv[1]).run()
    print(response.content)
