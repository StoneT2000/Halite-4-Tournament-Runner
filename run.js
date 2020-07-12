const Dimension = require('dimensions-ai');
let Tournament = Dimension.Tournament;
let Logger = Dimension.Logger;

// Setup the halite 4 envionment and integrate with dimensions-ai
let pathtorunner = "./run.sh";
let halite4 = Dimension.Design.createCustom('halite4', {
  resultHandler: (res) => {
    try {
      // we run only one episode, so we take the first element
      let rewards = JSON.parse(res[0])[0]
      rewards = rewards.map((r, index) => {
        return {
          agentID: index,
          score: r
        }
      });
      rewards.sort((a, b) => b.score - a.score)
      let results = rewards.map((info, index) => {
        return {
          agentID: info.agentID,
          rank: index + 1
        }
      });
      return {ranks: results}
    } catch(err) {
      console.error('Unexpected results', res);
      return {ranks: [], message: 'match error!'};
    }
  },
  command: pathtorunner,
  arguments: ['D_FILES']
});

// Create the dimension with the halite 4 environment
let halite4Dimension = Dimension.create(halite4, {
  name: 'Halite 4 Dimension',
  observe: false,
  activateStation: false // turns off the API
})

/**
 * The participating competitors, add and remove from this list and provide a 
 * path to the file for the agent and a identifying name 
 * e.g { file: "path/to/bot.py", name: "my_name" }
 */ 
let botlist = [
  { file: "./bots/still.py", name: "stillbot-1" },
  { file: "./bots/still.py", name: "stillbot-2" },
  { file: "./bots/swarm.py", name: "swarm" }, 
  { file: "./bots/bot.py", name: "somebot" }
]

// Create our tournament
let tourney = halite4Dimension.createTournament(botlist, {
  type: Tournament.TOURNAMENT_TYPE.LADDER,
  name: 'Your Halite 4 Trueskill Ladder',
  rankSystem: Tournament.RANK_SYSTEM.TRUESKILL, // change to Tournament.RANK_SYSTEM.ELO for ELO ranking
  loggingLevel: Logger.LEVEL.WARN,
  consoleDisplay: true,
  defaultMatchConfigs: {
    loggingLevel: Logger.LEVEL.NONE,
    storeErrorLogs: true // change to false to stop generating error logs from matches
  },
  resultHandler: (res) => {
    return {ranks: res.ranks};
  },
  agentsPerMatch: [2, 4],
  tournamentConfigs: {
    maxConcurrentMatches: 4,
    storePastResults: false
  }
});
// run the tournament
tourney.run();