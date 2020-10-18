from youtube_search import YoutubeSearch
import json 

results = YoutubeSearch('bleach OST', max_results=10).to_json()


json_object = json.loads(results)
json_formatted_str = json.dumps(json_object, indent=2)


print(json_formatted_str)

