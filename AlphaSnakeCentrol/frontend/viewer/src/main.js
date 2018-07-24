import GameRenderer from "./GameRenderer";
import SnakeTest from "./test/SnakeTest"


function main() {
	let canvas = document.getElementById("mycanvas"),
		ctx = canvas.getContext("2d");

	canvas.addEventListener("mousedown", (e) => {
		if (GameRenderer.Instance == null) {
			return;
		}

		const mouseX = e.offsetX,  mouseY = e.offsetY;
		const margin = 50;

		if (mouseX < margin) {
			GameRenderer.Instance.movDirX = GameRenderer.VIEWPORT_MOV_DIR_LEFT;
		} else if (mouseX > canvas.width - margin) {
			GameRenderer.Instance.movDirX = GameRenderer.VIEWPORT_MOV_DIR_RIGHT;
		}

		if (mouseY < margin) {
			GameRenderer.Instance.movDirY = GameRenderer.VIEWPORT_MOV_DIR_TOP;
		} else if (mouseY > canvas.height - margin) {
			GameRenderer.Instance.movDirY = GameRenderer.VIEWPORT_MOV_DIR_BOTTOM;
		}
	});

	canvas.addEventListener("mouseup", (e) => {
		if (GameRenderer.Instance == null) {
			return;
		}

		GameRenderer.Instance.movDirX = GameRenderer.VIEWPORT_MOV_DIR_NONE;
		GameRenderer.Instance.movDirY = GameRenderer.VIEWPORT_MOV_DIR_NONE;
	});

	connectServer();

	let renderer = new GameRenderer(ctx, canvas.width, canvas.height);

	// test
	// let test = new SnakeTest();

	// for (let i = 0; i < 10; i++) {
	// 	test.addSnake();
	// }

	requestAnimationFrame(update);
}

function connectServer() {
	const socket = io.connect("http://as.chinacloudsites.cn");
	socket.on("connect", function(data) {
		console.log("Socket Connected");
	});
	socket.on("judged", function(data) {
		console.log(data);
		console.log("Judged Message");

		GameRenderer.Instance.updateBoardData(data.map);
	});
}

function update() {
	if (SnakeTest.Instance != null) {
		SnakeTest.Instance.run();

		GameRenderer.Instance.updateBoardData(SnakeTest.Instance.map);
	}

	GameRenderer.Instance.update();

	requestAnimationFrame(update);
}

window.addEventListener("load", () => {
	main();
});