ball = require("ball")
map = require("map")

serial = require("serial")

local baudRate = 9600
local dataBits = 8
local stopBits = 1
local parity = 0
local portName = '/dev/ttyUSB0'

local fd = io.open(portName, 'r+')


playerA = {
    width = 10,
    -- height = 80,
    height = map.height,
    -- y = 200,
    y = 20,
    x = 580,
    score = 0
}

playerB = {
    width = 10,
    height = 80,
    y = 200,
    x = 40,
    score = 0
}


-- sound = love.audio.newSource("pong.wav")

scoreFont = love.graphics.newFont(30)

function love.update()
    ball.x = ball.x + ball.vel.x
    ball.y = ball.y + ball.vel.y

    -- map boundaries
    if ball.x >= (map.width + map.offset) - ball.width then
        playerB.score = playerB.score + 1
        ball:reset()
    end
    if ball.x <= map.offset then
        playerA.score = playerA.score + 1
        ball:reset()
    end

    -- walls bounce
    if ball.y <= map.offset then
        ball:bounce(1, -1)
    end
    if ball.y >= (map.height + map.offset) - ball.height then
        ball:bounce(1, -1)
    end

    -- paddles bounces
    if ball.x > playerA.x - ball.width and ball.y <= playerA.y + playerA.height and ball.y >= playerA.y - ball.height then
        ball:bounce(-1, 1)
        ball.x = ball.x - 10
    end
    if ball.x < playerB.x + 5 and ball.y <= playerB.y + playerB.height and ball.y >= playerB.y - ball.height then
        ball:bounce(-1, 1)
        ball.x = ball.x + 10
    end

    -- keys testing
    -- if love.keyboard.isDown("up") and playerA.y > map.offset then
    --     playerA.y = playerA.y - 2
    -- end
    -- if love.keyboard.isDown("down") and playerA.y + playerA.height < map.height + map.offset then
    --     playerA.y = playerA.y + 2
    -- end
    if love.keyboard.isDown("w") and playerB.y > map.offset then
        playerB.y = playerB.y - 2
    end
    if love.keyboard.isDown("s") and playerB.y + playerB.height < map.height + map.offset then
        playerB.y = playerB.y + 2
    end
end

function love.draw()
    love.graphics.rectangle("fill", ball.x, ball.y, ball.width, ball.height)
    love.graphics.rectangle("line", map.offset, map.offset, map.width, map.height)

    -- draw paddles
    love.graphics.rectangle("fill", playerA.x, playerA.y, playerA.width, playerA.height)
    love.graphics.rectangle("fill", playerB.x, playerB.y, playerB.width, playerB.height)

    love.graphics.setFont(scoreFont)
    -- draw score
    love.graphics.print(playerB.score .. " - " .. playerA.score, 280, 40)
end
