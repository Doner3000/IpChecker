# IpChecker
is a Python script, which takes input in form of either a CSV file, or a list of IP adresses and checks these against AbuseIPDB. In one of the future updates, there will be a function, which allows you to do an additional check against Virustotal database. For now I only implemented AbuseIPDB, since they allow way more API requests with a free account. This is also a reason why AbuseIPDB will probably always be prioritized by the script. Requires Python version 3.10 or later.

## How to use
1. Install Python version 3.10 or later, if you didn't already.
2. Install following packages using pip if not present on the system: re, json, csv, requests, os.
3. Start the script and enjoy using it.
