import turtle
import random


heart_color = "red" # กำหนดสีของหัวใจ
# สร้างหัวใจ
heart = turtle.Turtle()
heart.shape("heart")
heart.color(heart_color)
# กำหนดตำแหน่งเริ่มต้นของหัวใจ
heart.penup()
heart.setposition(0, 0)

# ฟังก์ชันที่จะสร้างการเคลื่อนไหวของหัวใจ
def beat():
    # เปลี่ยนขนาดของหัวใจ
    heart.scale(1 + random.uniform(-0.1, 0.1))

    # เลื่อนหัวใจขึ้นและลง
    heart.penup()
    heart.setposition(heart.xcor(), heart.ycor() + random.uniform(-5, 5))
    heart.pendown()

# เรียกใช้ฟังก์ชัน beat ซ้ำๆ
def main():
    while True:
        beat()
        turtle.delay(100)

if __name__ == "__main__":
    main()