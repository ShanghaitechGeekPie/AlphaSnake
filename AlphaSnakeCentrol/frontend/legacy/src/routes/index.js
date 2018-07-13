import React, { PropTypes } from 'react';
import { Router, Route, IndexRoute, Link } from 'react-router';
import { ContainerApp, IndexApp, App } from '../components/App';
import NotFound from '../components/NotFound';

const Routes = ({ history }) =>
  <Router history={history}>
    <Route path="/" component={ContainerApp}>
      <IndexRoute component={App}/>
      <Route path=":level1" component={App} />
      <Route path="*" component={NotFound}/>
    </Route>
    <Route path="*" component={NotFound}/>
  </Router>;

Routes.propTypes = {
  history: PropTypes.any,
};

export default Routes;
