# MegaKeep

Simple command-line application to "touch" your Mega accounts and avoid getting closed due to inactivity.

## How to use?
- run "pip install -r requirements.txt"
- ensure you have a space separated mega.txt in the root folder of the repository.
- run main.py

You can add comments to each account's line, an example would be: </br>
account@account.com SuperToughPasswordHere #Golden Girls S1-3

While it runs, it will create a log file in this format in the logs/raw folder: </br>
2023-11-25 21:52:10,299 Account account@account.com touched. Quota: 20480.0, Space used: {'used': 16285.399144172668, 'total': 20480.0} MB </br>
2023-11-25 21:52:13,576 Account account2@account.com touched. Quota: 20480.0, Space used: {'used': 15543.904494285583, 'total': 20480.0} MB

Once it has completed running, it will create a report in logs/reports: </br>
Each report will be structured like this:

MegaKeep Account Changes Report

Total space used: xxxx.xx GB </br>
Total Space available: xxxx.xx GB

Summary: </br>
Added: xxx accounts </br>
&nbsp;&nbsp;&nbsp;&nbsp;Content Increased: xxx accounts </br>
&nbsp;&nbsp;&nbsp;&nbsp;Content Decreased: xxx accounts </br>
&nbsp;&nbsp;&nbsp;&nbsp;Unchanged: xxx accounts </br>

Added: </br>
&nbsp;&nbsp;&nbsp;&nbsp;accountAdded@account.com - Space used: 14.40 GB, Space remaining: 5.60 GB

Content Increased: </br>
&nbsp;&nbsp;&nbsp;&nbsp;accountIncreased@account.com - Space used: 13.18 GB, Space remaining: 6.82 GB

Content Decreased: </br>
&nbsp;&nbsp;&nbsp;&nbsp;accountDecreased@account.com - Space used: 10.26GB, Space remaining: 9.74 GB

Unchanged: </br>
&nbsp;&nbsp;&nbsp;&nbsp;accountUnchanged@account.com - Space used: 17.09 GB, Space remaining: 2.91 GB


What I hope to do is add a little functionality to the script. If you have previously added accounts, you'll see them, if an account you previously had is no longer there, it will let you know that. If you have increased the content or decreased the content, you'll see that too.

Enjoy!!
