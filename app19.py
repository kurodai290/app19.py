import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="絶望要塞風 ブロック崩し", layout="centered")

st.title("密室脱出：セキュリティ・ハッキング")
st.caption("迫り来るレーザー（ブロック）をすべて破壊し、脱出ゲートを開け！")

# JavaScript & HTML5 Canvas によるブロック崩しコード
game_code = """
<div style="text-align: center; font-family: monospace;">
    <canvas id="gameCanvas" width="480" height="400" style="background: #111; border: 4px solid #00ff00; box-shadow: 0 0 20px #00ff00;"></canvas>
    <div id="status" style="color: #00ff00; font-size: 20px; margin-top: 10px; height: 30px;">SCORE: 0</div>
    <!-- 確実にリロードするためのHTMLボタンを追加 -->
    <button id="retryBtn" style="background: #000; color: #00ff00; border: 2px solid #00ff00; padding: 8px 20px; font-size: 16px; font-family: monospace; cursor: pointer; margin-top: 10px; box-shadow: 0 0 10px #00ff00; border-radius: 4px;">
        SYSTEM REBOOT (再挑戦)
    </button>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const statusDiv = document.getElementById("status");
const retryBtn = document.getElementById("retryBtn");

let animationId; // アニメーション管理用

// パドル（プレイヤー）
let paddleHeight = 10;
let paddleWidth = 75;
let paddleX;
let rightPressed = false;
let leftPressed = false;

// ボール
let ballRadius = 6;
let x, y, dx, dy;

// ブロック（防衛レーザー壁）
let brickRowCount = 5;
let brickColumnCount = 6;
let brickWidth = 65;
let brickHeight = 20;
let brickPadding = 10;
let brickOffsetTop = 40;
let brickOffsetLeft = 20;
let score;
let bricks = [];

// キーボード操作の登録（一度だけ実行）
if (!window.keyEventsRegistered) {
    document.addEventListener("keydown", (e) => {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
    }, false);
    document.addEventListener("keyup", (e) => {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
    }, false);
    window.keyEventsRegistered = true;
}

// ゲームの状態を初期化する関数
function initGame() {
    // 進行中のループがあれば停止
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    
    // パラメータのリセット
    paddleX = (canvas.width - paddleWidth) / 2;
    x = canvas.width / 2;
    y = canvas.height - 30;
    dx = 3;
    dy = -3;
    score = 0;
    statusDiv.innerHTML = "SCORE: 0";
    statusDiv.style.color = "#00ff00";

    // ブロックの再生成
    for (let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 };
        }
    }
    
    // ループ開始
    draw();
}

// リトライボタンが押されたら初期化
retryBtn.addEventListener("click", initGame);

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
                        statusDiv.style.color = "#00ffff";
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

    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) dx = -dx;
    if (y + dy < ballRadius) dy = -dy;
    else if (y + dy > canvas.height - ballRadius - 5) {
        if (x > paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
        } else {
            statusDiv.innerHTML = "GAME OVER：身柄が拘束されました";
            statusDiv.style.color = "#ff0000";
            dx = 0; dy = 0;
            return;
        }
    }

    if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 5;
    else if (leftPressed && paddleX > 0) paddleX -= 5;

    x += dx;
    y += dy;
    animationId = requestAnimationFrame(draw);
}

// 初回起動
initGame();
</script>
"""

# Streamlitアプリにゲームを埋め込み
components.html(game_code, height=520)

st.sidebar.markdown("""
### 操作方法
* **← / → キー**：パドルを移動
* **SYSTEM REBOOT ボタン**：ゲームを最初からやり直す
""")
