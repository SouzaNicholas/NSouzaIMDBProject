import requests

# API key stored in text file to keep it private from Github
def main():
    with open('secret.txt', 'r') as s:
        key = s.readline()
    dict = fetchTop250(key)
    outputRatings(key, dict)
    outputData(dict)


def fetchSeries(key: str, title: str) -> dict:
    series = requests.get(f"https://imdb-api.com/en/API/SearchTitle/{key}/{title}")
    return dict(series.json())

# I included a print statement here to illustrate an issue with the API.
# The total rating only appears as 0. The only useful information returned
# from a user rating API call is the spread of user votes on a 10-point scale
def fetchUserRating(key: str, id: str) -> str:
    rating = requests.get(f"https://imdb-api.com/en/API/UserRatings/{key}/{id}")
    print(rating.json())
    return rating.json()["totalRating"]


def fetchTop250(key) -> dict:
    top = requests.get(f"https://imdb-api.com/en/api/Top250TVs/{key}")
    json = parseJSON(top.json())
    return json

# Deciphers JSON to return a 'cleaned' version for Python
def parseJSON(data_dict: dict) -> dict:
    clean = {}
    for i in range(1, len(data_dict['items']) + 1):
        clean[i] = data_dict['items'][i - 1];
    return clean

# Was going to use f strings for file writing, but it caused issues with the dict keys
# being in quotation marks
def outputRatings(key, data_dict):
    with open("titles.txt", 'w') as f:
        WoT = fetchSeries(key, "The Wheel of Time")['results'][0]
        f.write(WoT["title"] + " - Rating: " + fetchUserRating(key, WoT["id"]) + '\n')
        f.write(data_dict[1]["title"] + " - Rating: " + fetchUserRating(key, data_dict[1]["id"]) + '\n')
        f.write(data_dict[50]["title"] + " - Rating: " + fetchUserRating(key, data_dict[50]["id"]) + '\n')
        f.write(data_dict[100]["title"] + " - Rating: " + fetchUserRating(key, data_dict[100]["id"]) + '\n')
        f.write(data_dict[150]["title"] + " - Rating: " + fetchUserRating(key, data_dict[150]["id"]) + '\n')
        f.write(data_dict[200]["title"] + " - Rating: " + fetchUserRating(key, data_dict[200]["id"]) + '\n')
        f.write(data_dict[250]["title"] + " - Rating: " + fetchUserRating(key, data_dict[250]["id"]) + '\n')



def outputData(data_dict):
    with open("titles.txt", 'a') as f:
        for v in data_dict.values():
            f.write(str(v))
            f.write('\n')
            print(v)


if __name__ == '__main__':
    main()
