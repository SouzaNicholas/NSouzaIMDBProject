Developed By: Nicholas Souza

Downloading the files from Github should be enough to run it. You'll only need to 
provide your own API key stored in a local file named "secret.txt"

The project will fetch your API key and use it to query the imDb API for the
Top 250 shows followed by the ratings for "The Wheel Of Time" and the 1st, 50th, 100th, 
150th, 200th, and 250th top rated shows. That data will be written out to "titles.txt"
with the ratings listed at the top of the file.

I'm having some issues with passing the linter. It's taking issue with the existence of
unicode in some overhead files that I do not recognize.