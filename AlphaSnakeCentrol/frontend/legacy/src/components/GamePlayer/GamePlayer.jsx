import React, { Component, PropTypes } from 'react';
import { Button, Spin, Icon, Row, Col } from 'antd';
import classnames from 'classnames';
import Mapnode from './Mapnode/Mapnode'
import PlayerCard from './PlayerCard/PlayerCard'
import styles from './GamePlayer.less';
const ButtonGroup = Button.Group;

class GamePlayer extends Component {
  state = {
      loaded: false,
      step: 0,
      autoPlay: false,
      data: undefined,
    }
  map = []
  constructor() {
    super();
    for (let i = 0; i < 102; i++) {
      for (let j = 0; j < 102; j++) {
        this.map.push(<Mapnode ref={"Mapnode" + i*102+j} key={i*102+j} x={i} y={j} border={(i==0)|(i==101)|(j==0)|(j==101)} />);
      }
    }
  }
  getRemoteDate() {
    fetch("http://127.0.0.1:8000/get_step/?gameid=1")
      .then(function(res) {
        if (res.ok) {
          res.json().then(function(data) {
            if (data.code == "success") {
              this.setState({
                data: data.step
              });
              console.log(this.state.data);
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
  nextStep() {
    let lastStep = this.state.step;
    let nextStep = this.state.step + 1;
    let allPlayers = this.state.data.length;
    let nextVisit = false;
    for (let j = 0; j < allPlayers; j++) {
      let allSteps = this.state.data[j].steps.length;

      if (nextStep <= allSteps) {
        nextVisit = true;
        let mapNodeID = "Mapnode" + (101 - this.state.data[j].steps[lastStep].y) * 102 + (this.state.data[j].steps[lastStep].x);
        let tNode =this.refs[mapNodeID];
        tNode.markActive(false);

        if (nextStep < allSteps) {
          let mapNodeID = "Mapnode" + (101 - this.state.data[j].steps[nextStep].y) * 102 + (this.state.data[j].steps[nextStep].x);
          let tNode =this.refs[mapNodeID];
          tNode.markFlag(j, nextStep);
          tNode.markActive(true);
        }
      }
    }

    if (nextVisit)
      this.setState({
        step: this.state.step + 1
      });
    else
      this.pauseStep();
  }
  previousStep() {
    let lastStep = this.state.step;
    let nextStep = this.state.step - 1;
    let allPlayers = this.state.data.length;
    for (let j = 0; j < allPlayers; j++) {
      let allSteps = this.state.data[j].steps.length;

      if (lastStep <= allSteps) {
        var mapNodeID = "Mapnode" + (101 - this.state.data[j].steps[nextStep].y) * 102 + (this.state.data[j].steps[nextStep].x);
        var tNode =this.refs[mapNodeID];
        tNode.markActive(true);

        if (lastStep < allSteps) {
          let mapNodeID = "Mapnode" + (101 - this.state.data[j].steps[lastStep].y) * 102 + (this.state.data[j].steps[lastStep].x);
          let tNode =this.refs[mapNodeID];
          tNode.unmarkFlag(lastStep);
          tNode.markActive(false);
        }
      }
    }

    if (nextStep >= 0)
      this.setState({
        step: this.state.step - 1
      })
  }
  reloadStep() {
    let lastStep = this.state.step;
    let allPlayers = this.state.data.length;
    for (let j = 0; j < allPlayers; j++) {
      let allSteps = this.state.data[j].steps.length;

      for (let i = 0; i < allSteps; i++) {
        var mapNodeID = "Mapnode" + (101 - this.state.data[j].steps[i].y) * 102 + (this.state.data[j].steps[i].x);
        var tNode =this.refs[mapNodeID];
        tNode.unmarkFlag(i);
        tNode.markActive(false);
      }
    }

    this.setState({
      step: 0
    })
  }
  playStep() {
    let t =
    this.setState({
      autoPlay: setInterval(this.nextStep.bind(this), 1000)
    })
  }
  pauseStep() {
    clearInterval(this.state.autoPlay);
    this.setState({
      autoPlay: undefined
    })
  }
  render() {
    if (this.state.data == undefined) {
      this.getRemoteDate();
    }
    return (
      <div className={styles.container}>
        <div className={styles.mapCantainer}>
          <div className={styles.map}>
            {this.map}
          </div>
        </div>
        <div className={styles.controlCantainer}>
          <ButtonGroup>
            <Button onClick={this.previousStep.bind(this)}>
              <Icon type="step-backward" />
            </Button>

            {(this.state.autoPlay) ?
              <Button onClick={this.pauseStep.bind(this)}>
                <Icon type="pause" />
              </Button>
              :
              <Button onClick={this.playStep.bind(this)}>
                <Icon type="caret-right" />
              </Button>
            }
            {(this.state.step == 0) ?
              null
              :
              <Button onClick={this.reloadStep.bind(this)}>
                <Icon type="reload" />
              </Button>
            }

            <Button onClick={this.nextStep.bind(this)}>
              <Icon type="step-forward" />
            </Button>
          </ButtonGroup>
          <div className={styles.counter}>
            Step: {this.state.step}
          </div>
          <PlayerCard data={this.state.data} step={this.state.step}/>
        </div>
      </div>
    );
  }
};

export default GamePlayer;
