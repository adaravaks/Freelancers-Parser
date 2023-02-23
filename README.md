# Freelancers-Parser
I have parsed through the list of freelancers on a popular russian topic-related website called 'Habr Freelance'

Libraries used: requests, json, time, beautifulsoup4, lxml, fake_useragent.

The parser works only with the first hundred pages of the list of freelancers, because parsing them all (more than 4700) would be too long and pointless for such a project. But if someone really needs it, then you can parse absolutely everyone, just change 101 in for-loop to the 'last-page-number' + 1

In order not to oversend the site with requests, I used one request for each page to be saved into an html file, and then I worked with these saved copies. Also, to make itself look more human-like, parser randomly generates a User_agent for itself at every iteration, and there is a 2-second pause between the iterations themselves.

For each freelancer, I have found:
- Name
- Specialization
- Positive ratings
- Negative ratings
- Work price
- 'About me' text
- Portfolio projects (if they exist)
- Selected tags

Then I filled all this into a json file, which turned out to be 46 thousand lines long (from just 100 pages! all of them would take about 2 mil. lines). By the way, I myself am between lines 9435 and 9454.
