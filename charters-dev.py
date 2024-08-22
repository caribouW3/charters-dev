import requests
import json

res = requests.get("https://api.github.com/repos/w3c/strategy/issues?state=open&labels=charter&per_page=100")

issues_list = json.loads(res.text)

fields = {'url','html_url', 'title','created_at','labels'}
issues = [{ k:v for (k,v) in issue.items() if k in fields} for issue in issues_list]


for i in issues:
	i["state"] = "emerging"
	i["review_link"] = ""
	for l in i["labels"]:
		if l["name"] == "Council":
			i.update({"state":"Council"})
			break
		elif l["name"] == "Horizontal review requested" and i["state"] != "AC review":
			i.update({"state":"HR"})
		elif l["name"] == "AC review":
			i.update({"state":"AC review"})
			# add code to find the email
			comments = requests.get(i["url"]+"/comments")
			comments_list = json.loads(comments.text)
			field = {"body"}
			for comment in comments_list:
				if "AC Review started" in comment["body"]:
					review_link = comment["body"]
			i.update({"review_link":review_link})
			#link = requests.get("https://www.w3.org/Search/Mail/Member/advanced_search?keywords="+ i["html_url"] + "&hdr-1-name=subject&hdr-1-query=VOTE&hdr-2-name=from&hdr-2-query=&hdr-3-name=message-id&hdr-3-query=&period_month=&period_year=&index-grp=Team__FULL+Member__FULL+Public__FULL&index-type=t&type-index=w3c-ac-members&resultsperpage=1&sortby=date#results")
			# probably gets a 401.
		elif l["name"] == "Advance Notice Sent" and i["state"] == "emerging":
			i.update({"state":"Advance notice"})
	#del i["labels"]
	fields = {'name'}
        l = [{k:v for (k,v) in label.items() if k in fields} for label in i["labels"]]
        i.update({"labels":l})
	#print (i['title']+' '+i['state'])

# Show json
#json_output = json.dumps(issues)
#print (json_output)

with open('charters-dev.json', 'w', encoding='utf-8') as f:
    json.dump(issues, f, ensure_ascii=False, indent=4)
