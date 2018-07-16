import React, { Component, PropTypes } from 'react';
import GamePlayer from './GamePlayer/GamePlayer';
import MainLayout from '../layouts/MainLayout/MainLayout';

class ContainerApp extends Component {
  render() {
    return (
      <MainLayout>
        {this.props.children}
      </MainLayout>
    );
  }
};

const IndexApp = ({ location }) => {
  return (
    <MainLayout>
      <GamePlayer location={location} />
    </MainLayout>
  );
};

const App = ({ location }) => {
  return (
    <GamePlayer location={location} />
  );
};

export default {
  'ContainerApp': ContainerApp,
  'IndexApp': IndexApp,
  'App': App
};
