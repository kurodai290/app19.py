import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="絶望要塞風 ブロック崩し", layout="centered")

st.title("密室脱出：セキュリティ・ハッキング")
st.caption("迫り来るレーザー（ブロック）をすべて破壊し、脱出ゲートを開け！")

# JavaScript & HTML5 Canvas によるブロック崩しコード
game_code = """
<div style="text-align: center;">
    <canvas id="gameCanvas" width="480" height="400" style="background: #111; border: 4px solid #00ff00; box-shadow: 0 0 20px #00ff00;"></canvas>
    <div id="status" style="color: #00ff00; font-family: monospace; font-size: 20px; margin-top: 10px;">SCORE: 0</div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const statusDiv = document.getElementById("status");

// パドル（プレイヤー）
let paddleHeight = 10;
let paddleWidth = 75;
let paddleX = (canvas.width - paddleWidth) / 2;
let rightPressed = false;
let leftPressed = false;

// ボール（ハッキングプログラム）
let ballRadius = 6;
let x = canvas.width / 2;
let y = canvas.height - 30;
let dx = 3;
let dy = -3;

// ブロック（防衛レーザー壁）
let brickRowCount = 5;
let brickColumnCount = 6;
let brickWidth = 65;
let brickHeight = 20;
let brickPadding = 10;
let brickOffsetTop = 40;
let brickOffsetLeft = 20;
let score = 0;

let bricks = [];
for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];
    for (let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
}

// キーボード操作
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
    else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
}
function keyUpHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
    else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
}

// 衝突判定
function collisionDetection() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            let b = bricks[c][r];
            if (b.status == 1) {
                if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                    dy = -dy;
                    b.status = 0;
                    score += 10;
                    statusDiv.innerHTML = "SCORE: " + score;
                    if (score == brickRowCount * brickColumnCount * 10) {
                        statusDiv.innerHTML = "脱出成功！セキュリティ解除！";
                        dx = 0; dy = 0;
                    }
                }
            }
        }
    }
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#00ff00";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight - 5, paddleWidth, paddleHeight);
    ctx.fillStyle = "#00ff00";
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            if (bricks[c][r].status == 1) {
                let brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                let brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                // 絶望要塞風の赤いレーザー壁
                ctx.fillStyle = "rgba(255, 0, 0, 0.8)";
                ctx.strokeStyle = "#ff0000";
                ctx.lineWidth = 1;
                ctx.stroke();
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    collisionDetection();

    // 壁との衝突判定
    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) dx = -dx;
    if (y + dy < ballRadius) dy = -dy;
    else if (y + dy > canvas.height - ballRadius - 5) {
        if (x > paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
        } else {
            statusDiv.innerHTML = "GAME OVER：身柄が拘束されました";
            dx = 0; dy = 0;
            return;
        }
    }

    // パドルの移動
    if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 5;
    else if (leftPressed && paddleX > 0) paddleX -= 5;

    x += dx;
    y += dy;
    requestAnimationFrame(draw);
}

draw();
</script>
"""

# Streamlitアプリにゲームを埋め込み
components.html(game_code, height=480)

st.sidebar.markdown("""
### 操作方法
* **← / → キー**：パドルを移動
* **リロード**：ゲームをやり直す
""")
