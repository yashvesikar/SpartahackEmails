To be honest around 1 AM I realized I should have just dumped the csv into a mysql db and just queried for all the info instead of doing all this csv manipulation. Also should have used `namedtuple()` but again, oh well.


Known bugs:
1. All names are lower case, I make it lower for comparison, however, for some reason, if I do not `.lower()` the name the data is not generated properly. The issue is somewhere in the cleanData function, most likely within the generates sponsor info section.

Please feel free to make pull requests and fix this code
