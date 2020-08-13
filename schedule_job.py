import requests


class ScrapyCloudJob:
    def run(self):
        return requests.post("https://app.scrapinghub.com/api/run.json?apikey=2018d259ee75404f93ad43dd8f236dbb",
                             data={"project": 468564, "spider": 'real_estate'})


if __name__ == "__main__":
    response = ScrapyCloudJob().run()
    print(response.content)
