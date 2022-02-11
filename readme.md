Developed By: Nicholas Souza

You'll need requests and sqlite3 installed to run the program. You'll only need to 
provide your own API key stored in a local file named "secret.txt"

The project has two tests to run. The first will validate that I query top 250 data
from the API properly. The second will create a dummy database and use my table
creation and population functions to fill the database.

My database test is currently failing, as I can't find a query that returns data in the
same format as the top 250 query. Otherwise, everything ought to be working fine. Once I
find an effective way to refactor my design, I'll be able to input shows from outside the
top 250 appropriately.