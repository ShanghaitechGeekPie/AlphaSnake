import { rgbToHsl, hslToRgb, hexToRgb } from "./color";
import { COLOR_LIST, ROW, COL, BLOCK_WIDTH, BLOCK_HEIGHT } from "./common";


const ELEMENT_NONE = "none";
const ELEMENT_FOOD = "food";
const ELEMENT_WALL = "wall";
const ELEMENT_HEAD = "head";
const ELEMENT_BODY = "body";

export default class GameRenderer {
	constructor(ctx, w, h) {
		GameRenderer.Instance = this;

		this.ctx = ctx;
		this.width = w;
		this.height = h;

		this.viewport = {x: 0, y: 0};
		this.movDirX = GameRenderer.VIEWPORT_MOV_DIR_NONE;
		this.movDirY = GameRenderer.VIEWPORT_MOV_DIR_NONE;

		this.boardData = [];
		this.isBoardDataUpdated = false;
	}

	updateBoardData(d) {
		this.boardData = d;

		this.isBoardDataUpdated = true;
	}

	update() {
		this.adjustViewport();

		this.ctx.save();

		this.ctx.translate(-this.viewport.x, -this.viewport.y);

		this.ctx.clearRect(0, 0, this.width, this.height);

		this.ctx.beginPath();
		this.ctx.fillStyle = "#000000";
		this.ctx.fillRect(0, 0, BLOCK_WIDTH * COL, BLOCK_HEIGHT * ROW);

		if (!this.isBoardDataUpdated) {
			return;
		}

		this.isBoardDataUpdated = false;

		for (let i = 0; i < ROW * COL; i++) {
			let v = this.boardData[i];
			let t = ELEMENT_NONE;

			if (v == -1) { // food
				t = ELEMENT_FOOD;
			} else if (v == -3) { // wall
				t = ELEMENT_WALL;
			} else if (v > 0 && v % 2 == 0) { // head
				t = ELEMENT_HEAD;
			} else if (v > 0 && v % 2 == 1) { // body
				t = ELEMENT_BODY;
			}

			if (t != ELEMENT_NONE) {
				this.drawElement(t, i, v);
			}
		}

		this.ctx.restore();
	}

	adjustViewport() {
		const movSpeed = 3;
		const minX = 0, maxX = -this.width + COL * BLOCK_WIDTH;
		const minY = 0, maxY = -this.height + ROW * BLOCK_HEIGHT;

		if (this.movDirX == GameRenderer.VIEWPORT_MOV_DIR_LEFT) {
			this.viewport.x -= movSpeed;
		} else if (this.movDirX == GameRenderer.VIEWPORT_MOV_DIR_RIGHT) {
			this.viewport.x += movSpeed;
		}

		if (this.movDirY == GameRenderer.VIEWPORT_MOV_DIR_TOP) {
			this.viewport.y -= movSpeed;
		} else if (this.movDirY == GameRenderer.VIEWPORT_MOV_DIR_BOTTOM) {
			this.viewport.y += movSpeed;
		}

		if (this.viewport.x < minX) {
			this.viewport.x = minX;
		} else if (this.viewport.x > maxX) {
			this.viewport.x = maxX;
		}

		if (this.viewport.y < minY) {
			this.viewport.y = minY;
		} else if (this.viewport.y > maxY) {
			this.viewport.y = maxY;
		}
	}

	drawElement(type, i, v) {
		let col = i % COL,
			row = (i - col) / COL;

		this.ctx.save();

		this.ctx.translate(col * BLOCK_WIDTH, row * BLOCK_HEIGHT);

		this.ctx.beginPath();

		if (type == ELEMENT_HEAD) {
			this.ctx.strokeStyle = "#FFFFFF";
			this.ctx.fillStyle = COLOR_LIST[v / 2];
			this.ctx.lineWidth = 2;

			this.ctx.rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT);
			this.ctx.arc(BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2, BLOCK_WIDTH / 4, 0, Math.PI);
			this.ctx.fill();
			this.ctx.stroke();
		} else if (type == ELEMENT_BODY) {
			this.ctx.strokeStyle = "#FFFFFF";
			this.ctx.fillStyle = COLOR_LIST[(v + 1) / 2];
			this.ctx.lineWidth = 2;

			this.ctx.rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT);
			this.ctx.fill();
			this.ctx.stroke();
		} else if (type == ELEMENT_WALL) {
			this.ctx.fillStyle = "#3F3F3F";

			this.ctx.rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT);
			this.ctx.fill();
		}

		this.ctx.restore();
	}
}

GameRenderer.Instance = null;

GameRenderer.VIEWPORT_MOV_DIR_NONE = -1;
GameRenderer.VIEWPORT_MOV_DIR_LEFT = 0;
GameRenderer.VIEWPORT_MOV_DIR_RIGHT = 1;
GameRenderer.VIEWPORT_MOV_DIR_TOP = 2;
GameRenderer.VIEWPORT_MOV_DIR_BOTTOM = 3;
