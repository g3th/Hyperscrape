# HyperScrape
## Problems/Code Scraper for HyperSkill
### Download your code locally, so that access isn't tied to a subscriprition.

What is the best site on the web for learning how to code? Hyperskill of course.

However, once your subscription expires you will not have the ability to look at your code for the problems and tasks you solved while your subscription was active.

Therefore, you will need to subscribe again to look at your code, comments and everything else tied to your account.

This script will allow you to download all solved problems, including tasks, locally so that you have access to your code whenever you want. It uses Selenium, so it is currently very slow, at approximately 6-10 seconds per problem downloaded. If, like me, you have been using the site extensively, downloading more than 200 problems could take a while.

I am hoping to add more functionality/options for future releases, such as the ability to download Theory attached to a particular problem, and generally speed up downloads by adding parallelization (i.e. concurrent.futures). Currently, only the links scraper uses threading.

The scraper requires a Hyperskill account.

