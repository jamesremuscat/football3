import * as React from 'react';
import { CSSProperties } from 'react';
import { Panel, Row, Col } from 'react-bootstrap';

import GameTime from './game-time';
import Game from '../model/game';
import Player from '../model/player';
import * as Palette from '../palette';
import { getLadderLeagueClass, formatRankChange, getNearlyInactiveClass } from '../utils/utils';

const statStyle: CSSProperties = {
  fontSize: 'x-large',
  fontWeight: 'bold',
  textAlign: 'center',
};

interface StatBoxProps {
  title: string;
  style?: CSSProperties;
  classes?: string;
  children?: any;
}
function StatBox(props: StatBoxProps): JSX.Element {
  const { title, children, style, classes } = props;
  const mergedStyle = style ? Object.assign({}, statStyle, style) : statStyle;
  return (
    <Panel header={<h3>{title}</h3>} style={mergedStyle} className={classes}>
      {children}
    </Panel>
  );
}

interface InstantStatBoxProps {
  title: string;
  at?: number;
  children?: any;
  base: string;
}
function InstantStatBox(props: InstantStatBoxProps): JSX.Element {
  const { title, at, children, base } = props;
  return (
    <Panel header={<h3>{title}</h3>}>
      <div style={statStyle}>{children}</div>
      <div style={{textAlign: 'right'}}>
        {at ? <span>at <GameTime date={at} base={base} /></span> : <span>before first game</span>}
      </div>
    </Panel>
  );
}

interface DurationStatBoxProps {
  title: string;
  from?: number;
  to?: number;
  children?: any;
  base: string;
}
function DurationStatBox(props: DurationStatBoxProps): JSX.Element {
  const { title, from, to, children, base } = props;
  return (
    <Panel header={<h3>{title}</h3>}>
      <div style={statStyle}>{children}</div>
      {from && <div style={{textAlign: 'right'}}>From <GameTime date={from} base={base} /></div>}
      {to && <div style={{textAlign: 'right'}}>to <GameTime date={to} base={base} /></div>}
    </Panel>
  );
}

interface RankStatBoxProps {
  rank: number;
  numActivePlayers: number;
  lastPlayed: number;
}
function RankStatBox(props: RankStatBoxProps): JSX.Element {
  const { rank, numActivePlayers, lastPlayed } = props;
  const now = (new Date()).getTime() / 1000;
  const league = getLadderLeagueClass(rank, numActivePlayers);
  const inactive = getNearlyInactiveClass(lastPlayed, now);
  const prettyRank = rank !== -1 ? rank : '-';
  return (
    <StatBox title="Current Ranking" style={{width: '100%'}} classes={`${league} ${inactive}`}>{prettyRank}</StatBox>
  )
}

interface SidePreferenceStatProps {
  player: Player;
}
function SidePreferenceStat(props: SidePreferenceStatProps): JSX.Element {
  const { player } = props;
  const redness = (player.total.gamesAsRed / player.total.games);
  const style = {
    backgroundColor: 'rgb(' + Math.round(redness * 255) + ', 0, '  + Math.round((1 - redness) * 255) + ')',
    color: 'white',
  };
  const pc = redness * 100;
  const preference = (pc >= 50) ? (pc.toFixed(2) + '% red') : ((100-pc).toFixed(2) + '% blue');
  return (
    <StatBox title='Side preference' style={style}>{preference}</StatBox>
  )
}

function getSkillRecords(player: Player, games: Game[]) {
  const skillLine = games.reduce((skillLine, game) => {
    const prevSkill = skillLine[skillLine.length - 1].skill;
    const change = game.red.name == player.name ? game.red.skillChange : game.blue.skillChange;
    skillLine.push({date: game.date, skill: (prevSkill + change)});
    return skillLine;
  }, [{date: 0, skill: 0}]);
  const highestSkill = skillLine.reduce((highest, skill) => skill.skill > highest.skill ? skill : highest, {date: 0, skill: 0});
  const lowestSkill = skillLine.reduce((lowest, skill) => skill.skill < lowest.skill ? skill : lowest, {date: 0, skill: 0});
  return {highestSkill, lowestSkill};
}

interface Streak {
  win: boolean;
  gameTimes: number[];
}
function getStreakRecords(player: Player, games: Game[]) {
  const { streaks, currentStreak } = games.reduce(({streaks, currentStreak}, game) => {
    const won = (game.red.name == player.name && game.red.score > game.blue.score) || (game.blue.name == player.name && game.blue.score > game.red.score);
    const lost = (game.red.name == player.name && game.red.score < game.blue.score) || (game.blue.name == player.name && game.blue.score < game.red.score);
    if ((won && currentStreak.win) || lost && !currentStreak.win) {
      currentStreak.gameTimes.push(game.date);
    }
    else {
      if (currentStreak.gameTimes.length > 0) {
        streaks.push(currentStreak);
      }
      currentStreak = {win: won, gameTimes: []};
      if (won || lost) {
        currentStreak.gameTimes.push(game.date);
      }
    }
    return {streaks, currentStreak};
  }, {streaks: [], currentStreak: {win: true, gameTimes: []}});
  const winningStreak = streaks.reduce((winning, streak) => (streak.win && streak.gameTimes.length > winning.gameTimes.length) ? streak : winning , {win: true, gameTimes: []});
  const losingStreak = streaks.reduce((losing, streak) => (!streak.win && streak.gameTimes.length > losing.gameTimes.length) ? streak : losing, {win: false, gameTimes: []});
  return {winningStreak, losingStreak, currentStreak};
}

interface PlayerStatsProps {
  player: Player;
  games: Game[];
  numActivePlayers: number;
  base: string;
}
export default function PlayerStats(props: PlayerStatsProps): JSX.Element {
  function isTenNilWin(playerName: string, game: Game): boolean {
    return (game.red.score == 10 && game.blue.score == 0 && game.red.name == playerName) ||
      (game.blue.score == 10 && game.red.score == 0 && game.blue.name == playerName);
  }
  function getOverrated(playerName: string, games: Game[]): number {
    let skill = 0;
    let total = 0;
    games.slice(games.length - 10).forEach((game) => {
      skill += game.red.name === playerName ? game.red.skillChange : game.blue.skillChange;
      total += skill;
    })
    return skill - (total / 10);
  }
  function getBG(blue: boolean): CSSProperties {
    return {backgroundColor: blue ? Palette.blueFade : Palette.redFade};
  }
  const { player, numActivePlayers, games, base } = props;
  const overrated = getOverrated(player.name, games);
  const gamesToday = games.slice(games.length - player.total.gamesToday);
  const goalRatio = player.total.for / player.total.against;
  const tenNils = games.reduce((count, game) => count += isTenNilWin(player.name, game) ? 1 : 0, 0);
  const skillChangeToday = gamesToday.reduce((skill, game) => skill += game.red.name == player.name ? game.red.skillChange : game.blue.skillChange, 0);
  const rankChangeToday = gamesToday.reduce((change, game) => change += game.red.name == player.name ? game.red.rankChange : game.blue.rankChange, 0);
  const { highestSkill, lowestSkill } = getSkillRecords(player, games);
  const { winningStreak, losingStreak, currentStreak } = getStreakRecords(player, games);
  return (
    <Panel header={<h1>{player.name}</h1>}>
      <Row>
        <Col sm={3}><RankStatBox rank={player.rank} numActivePlayers={numActivePlayers} lastPlayed={games[games.length - 1].date} /></Col>
        <Col sm={3}><StatBox title="Skill">{player.skill.toFixed(3)}</StatBox></Col>
        <Col sm={3}><StatBox title={'Overrated'} style={getBG(overrated >= 0)}>{overrated.toFixed(3)}</StatBox></Col>
        <Col sm={3}><SidePreferenceStat player={player}/></Col>
      </Row>
      <Row>
        <Col sm={3}><StatBox title="Total games">{player.total.games}</StatBox></Col>
        <Col sm={3}><StatBox title="Wins">{player.total.wins}</StatBox></Col>
        <Col sm={3}><StatBox title="Losses">{player.total.losses}</StatBox></Col>
        <Col sm={3}><StatBox title="Draws">{(player.total.games - player.total.wins - player.total.losses)}</StatBox></Col>
      </Row>
      <Row>
        <Col sm={3}><StatBox title="Goals for">{player.total.for}</StatBox></Col>
        <Col sm={3}><StatBox title="Goals against">{player.total.against}</StatBox></Col>
        <Col sm={3}><StatBox title="Goal ratio" style={getBG(goalRatio > 1)}>{goalRatio.toFixed(3)}</StatBox></Col>
        <Col sm={3}><StatBox title='10-0 wins'>{tenNils}</StatBox></Col>
      </Row>
      <Row>
        <Col sm={3}><StatBox title="Games today">{gamesToday.length}</StatBox></Col>
        <Col sm={3}><StatBox title="Skill change today" style={getBG(skillChangeToday >= 0)}>{skillChangeToday.toFixed(3)}</StatBox></Col>
        <Col sm={3}><StatBox title="Rank change today" style={getBG(rankChangeToday >= 0)}>{formatRankChange(rankChangeToday)}</StatBox></Col>
        <Col sm={3}/>
        <Col sm={3}>
          <DurationStatBox title={'Current streak'}
            from={currentStreak.gameTimes[0]}
            to={currentStreak.gameTimes[currentStreak.gameTimes.length - 1]}
            base={base}
          >
            {currentStreak.gameTimes.length > 0 ? `${currentStreak.gameTimes.length} ${currentStreak.win ? 'wins' : 'losses'}` : '-'}
          </DurationStatBox>
        </Col>
      </Row>
      <Row>
        <Col sm={3}><InstantStatBox title={'Highest ever skill'} at={highestSkill.date} base={base}>{highestSkill.skill.toFixed(3)}</InstantStatBox></Col>
        <Col sm={3}><InstantStatBox title={'Lowest ever skill'} at={lowestSkill.date} base={base}>{lowestSkill.skill.toFixed(3)}</InstantStatBox></Col>
        <Col sm={3}>
          <DurationStatBox
            title={'Longest winning streak'}
            from={winningStreak.gameTimes[0]}
            to={winningStreak.gameTimes[winningStreak.gameTimes.length - 1]}
            base={base}
          >
            {winningStreak.gameTimes.length || '-'}
          </DurationStatBox>
        </Col>
        <Col sm={3}>
          <DurationStatBox
            title={'Longest losing streak'}
            from={losingStreak.gameTimes[0]}
            to={losingStreak.gameTimes[losingStreak.gameTimes.length - 1]}
            base={base}
          >
            {losingStreak.gameTimes.length || '-'}
          </DurationStatBox>
        </Col>
      </Row>
    </Panel>
  );
}
