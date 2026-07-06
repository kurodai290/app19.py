import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="絶望要塞風 ブロック崩し", layout="centered")
st.title("🏰 絶望要塞風 ブロック崩し")
st.caption("制限時間内にすべてのターゲット（ブロック）を破壊し、要塞を脱出せよ！")

# HTML5 Canvas + JavaScript によるゲーム実装
game_code = """
<div style="text-align: center;">
    <canvas id="gameCanvas" width="480" height="400" style="background: #111; border: 4px solid #ff4b4b;"></canvas>
    <div id="status" style="font-family: sans-serif; color: white; margin-top: 10px; font-size: 20px; font-weight: bold;"></div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// ゲーム設定
let ballRadius = 8;
let x = canvas.width / 2;
let y = canvas.height - 30;
let dx = 3;
let dy = -3;

const paddleHeight = 10;
const paddleWidth = 75;
let paddleX = (canvas.width - paddleWidth) / 2;

let rightPressed = false;
let leftPressed = false;

// ブロック設定（要塞の防壁）
const rowCount = 4;
const columnCount = 5;
const brickWidth = 75;
const brickHeight = 20;
const brickPadding = 10;
const brickOffsetTop = 50;
const brickOffsetLeft = 30;

let bricks = [];
for (let c = 0; c < columnCount; c++) {
    bricks[c] = [];
    for (let r = 0; r < rowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
}

// 制限時間（秒）
let timeLeft = 45;
let gameStatus = "PLAYING"; // PLAYING, WIN, GAMEOVER

// タイマーカウントダウン
const timerInterval = setInterval(() => {
    if (gameStatus === "PLAYING") {
        timeLeft--;
        if (timeLeft <= 0) {
            gameStatus = "GAMEOVER";
            clearInterval(timerInterval);
        }
    }
}, 1000);

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
    let allDestroyed = true;
    for (let c = 0; c < columnCount; c++) {
        for (let r = 0; r < rowCount; r++) {
            let b = bricks[c][r];
            if (b.status === 1) {
                allDestroyed = false;
                if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                    dy = -dy;
                    b.status = 0;
                }
            }
        }
    }
    if (allDestroyed && gameStatus === "PLAYING") {
        gameStatus = "WIN";
        clearInterval(timerInterval);
    }
}

// 描画関数群
function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#00ffcc";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = "#ff4b4b";
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {
    for (let c = 0; c < columnCount; c++) {
        for (let r = 0; r < rowCount; r++) {
            if (bricks[c][r].status === 1) {
                let brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                let brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                ctx.fillStyle = r % 2 === 0 ? "#ffcc00" : "#ff3300";
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

function drawUI() {
    // タイマー描画
    ctx.font = "16px sans-serif";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("TIME LEFT: " + timeLeft + "s", 8, 25);
    
    // 要塞アラート風演出
    if (timeLeft <= 10) {
        ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (gameStatus === "PLAYING") {
        drawBricks();
        drawBall();
        drawPaddle();
        drawUI();
        collisionDetection();

        // 壁との衝突
        if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) dx = -dx;
        if (y + dy < ballRadius) dy = -dy;
        else if (y + dy > canvas.height - ballRadius) {
            if (x > paddleX && x < paddleX + paddleWidth) {
                dy = -dy;
            } else {
                gameStatus = "GAMEOVER";
                clearInterval(timerInterval);
            }
        }

        // パドル移動
        if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 5;
        else if (leftPressed && paddleX > 0) paddleX -= 5;

        x += dx;
        y += dy;
        requestAnimationFrame(draw);
    } else if (gameStatus === "WIN") {
        document.getElementById("status").innerHTML = "🔓 脱出成功！ミッションクリア！";
        ctx.fillStyle = "#00ffcc";
        ctx.font = "30px sans-serif";
        ctx.fillText("MISSION CLEAR", 120, 200);
    } else if (gameStatus === "GAMEOVER") {
        document.getElementById("status").innerHTML = "🚨 脱出失敗... 確保されました。";
        ctx.fillStyle = "#ff4b4b";
        ctx.font = "30px sans-serif";
        ctx.fillText("GAME OVER", 150, 200);
    }
}

draw();
</script>
"""

# Streamlitアプリに埋め込み
components.html(game_code, height=460)

st.info("💡 操作方法: キーボードの「←」「→」矢印キーで赤いパドルを動かします。")
