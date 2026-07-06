import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="絶望要塞風 ブロック崩し", layout="centered")

st.title("密室脱出：セキュリティ・ハッキング")
st.caption("迫り来るレーザー（ブロック）をすべて破壊し、脱出ゲートを開け！")

# 画面サイズの設定
canvas_width = 640
canvas_height = 480
component_height = canvas_height + 120  # ボタンやスコア表示の余白を含めた全体の高さ

# JavaScript & HTML5 Canvas によるブロック崩しコード
game_code = f"""
<div style="text-align: center; font-family: monospace;">
    <canvas id="gameCanvas" width="{canvas_width}" height="{canvas_height}" style="background: #111; border: 4px solid #00ff00; box-shadow: 0 0 20px #00ff00;"></canvas>
    <div id="status" style="color: #00ff00; font-size: 22px; margin-top: 15px; height: 35px; font-weight: bold;">SCORE: 0</div>
    <button id="retryBtn" style="background: #000; color: #00ff00; border: 2px solid #00ff00; padding: 10px 25px; font-size: 18px; font-family: monospace; cursor: pointer; margin-top: 10px; box-shadow: 0 0 10px #00ff00; border-radius: 4px;">
        SYSTEM REBOOT (再挑戦)
    </button>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const statusDiv = document.getElementById("status");
const retryBtn = document.getElementById("retryBtn");

let animationId;

// パドル（プレイヤー）※画面拡大に合わせて調整
let paddleHeight = 12;
let paddleWidth = 100;
let paddleX;
let rightPressed = false;
let leftPressed = false;

// ボール
let ballRadius = 8;
let x, y, dx, dy;

// ブロック（防衛レーザー壁）
let brickRowCount = 5;
let brickColumnCount = 7; 
let brickPadding = 12;
let brickOffsetTop = 50;
let brickOffsetLeft = 25;
let brickWidth = (canvas.width - (brickOffsetLeft * 2) - (brickPadding * (brickColumnCount - 1))) / brickColumnCount;
let brickHeight = 24;
let score;
let bricks = [];

if (!window.keyEventsRegistered) {{
    document.addEventListener("keydown", (e) => {{
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
    }}, false);
    document.addEventListener("keyup", (e) => {{
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
    }}, false);
    window.keyEventsRegistered = true;
}}

function initGame() {{
    if (animationId) {{
        cancelAnimationFrame(animationId);
    }}
    
    paddleX = (canvas.width - paddleWidth) / 2;
    x = canvas.width / 2;
    y = canvas.height - 40;
    dx = 4; 
    dy = -4;
    score = 0;
    statusDiv.innerHTML = "SCORE: 0";
    statusDiv.style.color = "#00ff00";

    for (let c = 0; c < brickColumnCount; c++) {{
        bricks[c] = [];
        for (let r = 0; r < brickRowCount; r++) {{
            bricks[c][r] = {{ x: 0, y: 0, status: 1 }};
        }}
    }}
    
    draw();
}}

retryBtn.addEventListener("click", initGame);

function collisionDetection() {{
    for (let c = 0; c < brickColumnCount; c++) {{
        for (let r = 0; r < brickRowCount; r++) {{
            let b = bricks[c][r];
            if (b.status == 1) {{
                if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {{
                    dy = -dy;
                    b.status = 0;
                    score += 10;
                    statusDiv.innerHTML = "SCORE: " + score;
                    if (score == brickRowCount * brickColumnCount * 10) {{
                        statusDiv.innerHTML = "脱出成功！セキュリティ解除！";
                        statusDiv.style.color = "#00ffff";
                        dx = 0; dy = 0;
                    }}
                }
            }}
        }}
    }}
}}

function drawBall() {{
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#00ff00";
    ctx.fill();
    ctx.closePath();
}}

function drawPaddle() {{
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight - 8, paddleWidth, paddleHeight);
    ctx.fillStyle = "#00ff00";
    ctx.fill();
    ctx.closePath();
}}

function drawBricks() {{
    for (let c = 0; c < brickColumnCount; c++) {{
        for (let r = 0; r < brickRowCount; r++) {{
            if (bricks[c][r].status == 1) {{
                let brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                let brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                ctx.fillStyle = "rgba(255, 0, 0, 0.8)";
                ctx.strokeStyle = "#ff0000";
                ctx.lineWidth = 1.5;
                ctx.stroke();
                ctx.fill();
                ctx.closePath();
            }
        }}
    }}
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    collisionDetection();

    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) dx = -dx;
    if (y + dy < ballRadius) dy = -dy;
    else if (y + dy > canvas.height - ballRadius - 8) {{
        if (x > paddleX && x < paddleX + paddleWidth) {{
            dy = -dy;
        }} else {{
            statusDiv.innerHTML = "GAME OVER：身柄が拘束されました";
            statusDiv.style.color = "#ff0000";
            dx = 0; dy = 0;
            return;
        }}
    }}

    if (rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 6;
    else if (leftPressed && paddleX > 0) paddleX -= 6;

    x += dx;
    y += dy;
    animationId = requestAnimationFrame(draw);
}}

initGame();
</script>
"""

# Streamlitアプリに埋め込み
components.html(game_code, height=component_height)

st.sidebar.markdown("""
### 操作方法
* **← / → キー**：パドルを移動
* **SYSTEM REBOOT ボタン**：ゲームを最初からやり直す
""")
