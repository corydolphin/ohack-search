# http://ohack-search.herokuapp.com

A simple flask application to allow students to search through MailMan archives, specifically targetted at Helpme. 

#TODO
* Authorization and IP-walling to ensure users are on campus needs to be finalized.
* Finish exposing a search API for easy integration into fwol.in via JSON


#Search API:
The search API is accessible from the /search route. Simply pass in a urlencoded query parameter, i.e. /search?query=hello
Output is JSON, format subject to change. Currently weird and nested.

```
{
  "emails": {
  "(Some Thread ID)" : [
  	{
  		"body":[
  			"Paragraph One of email One",
  			"Paragraph Two of email One"
  		],
  		"date": "Thu, 8 Nov 2012 17:32:40 -0500",
  		"threadId":"(Some Thread ID",
  		"subject": "Some subject"
  	}
  	{
  		"body":[
  			"Paragraph One of email Two",
  			"Paragraph Two of email Two"
  		],
  		"date": "Thu, 8 Nov 2012 18:32:40 -0500",
  		"threadId":"(Some Thread ID",
  		"subject": "R.E. Some subject"
  	}
  ]
}
```