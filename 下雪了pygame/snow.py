import pygame
import random
#初始化
pygame.init()
#根据图片设置屏幕大小
SIZE = (1280, 845)
screen = pygame.display.set_mode(SIZE)   #display显示
pygame.display.set_caption("下雪了")   #caption标题
background = pygame.image.load('snow.jpg')
#设置雪花
snow = []
for i in range(300):
    x = random.randrange(0, SIZE[0])
#random.randrange([start],stop[, step])：从指定范围内，按指定基数递增的集合中获取一个随机数。
    y = random.randrange(0, SIZE[1])
    speedx = random.randint(-1, 2)
#random.randint(a,b)：用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n：a<=n<=b。
    speedy = random.randint(3, 8)
    snow.append([x, y, speedx, speedy])

done = False
while not done:
    # 消息事件循环，判断退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # 绘制位图
    #screen.blit(space, (0,0))第一个参数是加载完成的位图，第二个参数是绘制的起始坐标。
    screen.blit(background, (0, 0))
    for i in range(len(snow)):
        # 绘制雪花，颜色、位置、大小
        #pygame.draw.circle(Surface, color, pos, radius, width=0)用于在Surface上绘制一些简单的图形，比如点、直线、矩形、圆、弧
        pygame.draw.circle(screen, (255, 255, 255), snow[i][:2], snow[i][3])  # x轴偏移量越大,雪球越大
        # 移动雪花位置（下一次循环起效）
        snow[i][0] += snow[i][2]
        snow[i][1] += snow[i][3]

        # 如果雪花落出屏幕，重设位置
        if snow[i][1] > SIZE[1]:
            snow[i][1] = random.randrange(-50, -10)
            snow[i][0] = random.randrange(0, SIZE[0])
    pygame.display.flip()  #刷新屏幕

pygame.quit()
