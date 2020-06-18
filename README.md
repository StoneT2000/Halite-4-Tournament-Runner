# Halite 4 Tournament Runner

This code allows you to run a local tournament ranking bots you provide by the Trueskill or ELO ranking algorithm (somewhat similar to the current Kaggle leaderboard ranking system)

Ensure you have [NodeJS](https://nodejs.org/) version 12.x or above installed

To run the tournament, fork this repo or clone it to your computer, and first install the following package
```
npm install dimensions-ai
```
then run
```
node.js
```

to see a live display of a leaderboard of 3 different bots. The sample bots used here for demonstration are the swarm bot by Yegor Biryukov: https://www.kaggle.com/yegorbiryukov/halite-swarm-intelligence and the getting started bot provided by Kaggle: https://www.kaggle.com/alexisbcook/getting-started-with-halite

the file `run.sh` has the command that is used to run the matches in the tournament, and to add more bots, add them to the list in `run.js` at line 47

To use ELO ranking instead of trueskill (the default), change line 58 in `run.js` to `Tournament.RANK_SYSTEM.ELO`

Unfortunately, Windows doesn't work, you will need WSL
