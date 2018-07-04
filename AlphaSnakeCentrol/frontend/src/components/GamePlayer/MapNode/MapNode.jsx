import React, { Component, PropTypes } from 'react';
import classnames from 'classnames';
import styles from './Mapnode.less';

class Mapnode extends Component {
  state = {
      active: false,
      step: undefined,
      status: undefined,
    }
  markActive(status) {
    this.setState({
      active: status
    })
  }
  markFlag(status, step) {
    if (this.state.status == undefined)
      this.setState({
        status: status,
        step: step
      })
  }
  unmarkFlag(step) {
    if (this.state.step == step)
      this.setState({
        status: undefined,
        step: undefined
      })
  }
  render() {
    const backgroundCls = classnames({
      [styles.container]: true,
      [styles.container_d]: (this.props.x + this.props.y)%2==0,
      [styles.container_l]: (this.props.x + this.props.y)%2!=0,
      [styles.container_border]: (this.props.border),
    });
    const innerCls = classnames({
      [styles.inner]: true,
      [styles.inner_0]: (this.state.status == 0),
      [styles.inner_1]: (this.state.status == 1),
      [styles.inner_2]: (this.state.status == 2),
      [styles.inner_3]: (this.state.status == 3),
      [styles.inner_active]: (this.state.active),
    });
    return (
      <div className={backgroundCls}>
        <div className={innerCls}></div>
      </div>
    );
  }
};

export default Mapnode;
