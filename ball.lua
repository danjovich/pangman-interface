module("ball")

ball = {
    x = 300,
    y = 200,
    vel = {
        x = 3,
        y = 1
    },
    height = 30,
    width = 30
}

function ball:bounce(x, y)
    self.vel.x = x * self.vel.x
    self.vel.y = y * self.vel.y
end

function ball:reset()
    ball.x = 300
    ball.y = 200
    ball.vel = {}
    ball.vel.x = 3
    ball.vel.y = 1
    ball.height = 30
    ball.width = 30
end

return ball
