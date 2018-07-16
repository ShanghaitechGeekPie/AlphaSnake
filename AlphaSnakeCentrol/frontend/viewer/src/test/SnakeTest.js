import { ROW, COL } from "../common";


export default class SnakeTest {
	constructor() {
		SnakeTest.Instance = this;

		this.snakeList = [];
		this.map = [];

		this.lag = 15;
		this.lagTick = 0;
	}

	initMap() {
		this.map.splice(0, this.map.length);

		for (let i = 0; i < ROW * COL; i++) {
			this.map.push(0);
		}
	}

	addSnake() {
		let s = new Snake();
		this.snakeList.push(s);
	}

	run() {
		if (this.lagTick++ < this.lag) {
			return;
		}

		this.lagTick = 0;

		this.initMap();

		for (let i = 0; i < this.snakeList.length; i++) {
			let snake = this.snakeList[i]
			snake.run();
			snake.putOnMap(this.map);
		}
	}
}

SnakeTest.Instance = null;


class Snake {
	constructor() {
		this.id = ++Snake.SNAKE_ID;

		this.list = [];

		this.initSnake();
	}

	initSnake() {
		let randomX = Math.floor(Math.random() * 100),
			randomY = Math.floor(Math.random() * 99) + 1;

		this.list.push([randomX, randomY]);
		this.list.push([randomX, randomY - 1]);
	}

	putOnMap(map) {
		for (let i = 0; i < this.list.length; i++) {
			const node = this.list[i], v = node[0] + node[1] * COL;

			if (i == 0) {
				map[v] = this.id * 2;
			} else {
				map[v] = this.id * 2 - 1;
			}
		}
	}

	run() {
		const dir = Math.floor(Math.random() * 4);
		const head = this.list[0];

		if (dir == 0) {
			this.list.splice(0, 0, [head[0] - 1, head[1]]);
		} else if (dir == 1) {
			this.list.splice(0, 0, [head[0] + 1, head[1]]);
		} else if (dir == 2) {
			this.list.splice(0, 0, [head[0], head[1] - 1]);
		} else if (dir == 3) {
			this.list.splice(0, 0, [head[0], head[1] + 1]);
		}

		this.list.pop();
	}
}

Snake.SNAKE_ID = 0;
