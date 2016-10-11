import * as React from 'react';
import { Component, Props } from 'react';
import { Grid, Row, Col } from 'react-bootstrap';
import * as ReactDOM from 'react-dom';
import 'whatwg-fetch';

import GameSummary from './components/game-summary';
import GameDetails from './components/game-details';
import NavigationBar from './components/navigation-bar';
import Game from './model/game';
import { getParameterByName } from './utils/utils';

interface GamePageProps extends Props<GamePage> {
  root: string;
  addURL: string;
  gameId: string;
}
interface GamePageState {
  game: Game;
}
class GamePage extends Component<GamePageProps, GamePageState> {
  constructor(props: GamePageProps, context: any) {
    super(props, context)
    this.state = {
      game: undefined,
    };
  }
  async load() {
    const { root, gameId } = this.props;
    const url = `${root}game.cgi?method=view&view=json&game=${gameId}`;
    const r = await fetch(url);
    this.setState({game: await r.json()});
  }
  componentDidMount() {
    this.load();
  }
  render() {
    const { root, addURL } = this.props;
    //TODO
    const numActivePlayers = 0;
    return (
      <div className="gamePage">
        <NavigationBar
          root={root}
          addURL={addURL}
        />
        {this.state.game ?
          <Grid fluid={true}>
            <Row>
              <GameSummary game={this.state.game} base={"../../"} numActivePlayers={numActivePlayers} />
            </Row>
            <Row>
              <GameDetails game={this.state.game} />
            </Row>
          </Grid>
          : 'Loading...'
        }
      </div>
    );
  }
};

ReactDOM.render(
    <GamePage
      root={'http://www/~tlr/tntfl-test/'}
      addURL={'game/add'}
      gameId={getParameterByName('game')}
    />,
    document.getElementById('entry')
);
