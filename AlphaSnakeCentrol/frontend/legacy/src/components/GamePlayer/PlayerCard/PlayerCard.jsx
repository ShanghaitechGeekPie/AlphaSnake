import React, { Component, PropTypes } from 'react';
import { Card, Icon } from 'antd';
import classnames from 'classnames';
import styles from './PlayerCard.less';

class Mapnode extends Component {
  state = {
      players: undefined,
    }
  getRemoteDate() {
    fetch("http://127.0.0.1:8000/info/?gameid=1&command=all")
      .then(function(res) {
        if (res.ok) {
          res.json().then(function(data) {
            if (data.code == "success") {
              this.setState({
                players: data.players
              });
              console.log(data);
            } else {
              console.log("Backend error", data.status);
            }
          }.bind(this));
        } else {
          console.log("Looks like the response wasn't perfect, got status", res.status);
        }
      }.bind(this), (e) => {
        console.log("Fetch failed!", e);
      });
  }
  render() {
    let t = [];
    if (this.state.players == undefined) {
      this.getRemoteDate();
    } else {
      let hackTable = {
        '-1':null,
        '0': <Icon type="circle-up" />,
        '1': <Icon type="circle-right" />,
        '2': <Icon type="circle-down" />,
        '3': <Icon type="circle-left" />,
      };
      if (this.props.data)
        for (let i = 0; i < this.props.data.length; i++) {
          const backgroundCls = classnames({
            [styles.choice]: true,
            [styles.choice_0]: (i == 0),
            [styles.choice_1]: (i == 1),
            [styles.choice_2]: (i == 2),
            [styles.choice_3]: (i == 3),
          });
          t.push(
            <div key={i}>
              <Card>
                <h1>{this.state.players[i].name}</h1>
                <h3>{this.state.players[i].team}</h3>
                <div className={backgroundCls}>
                  {(this.props.step <= this.props.data[i].steps.length - 1)?
                    hackTable[this.props.data[i].steps[this.props.step].choice]
                    :
                    this.props.data[i].steps.length - 1
                  }
                </div>
              </Card>
            </div>
          );
        }
    }
    return (
      <div className={styles.container}>
        {t}
      </div>
    );
  }
};

export default Mapnode;
