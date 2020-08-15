import requests
import sys


class ScrapyCloudJob:

    def __init__(self, to_scrap='all'):
        self.to_scrap = to_scrap

    def run(self):
        print(self.to_scrap)
        separator = ","
        return requests.post("https://app.scrapinghub.com/api/run.json?apikey=2018d259ee75404f93ad43dd8f236dbb",
                             data={"project": 468564, "spider": 'real_estate',
                                   "job_settings": f'{{"JOB_TYPE": "{separator.join(self.to_scrap)}"}}'})


if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        response = ScrapyCloudJob().run()
    else:
        provinces = [province.replace('_', ' ') for province in sys.argv[1:]]
        response = ScrapyCloudJob(to_scrap=provinces).run()
    print(response.content)
