# Tutorial

![](./localDemo.gif)

## Installation

To make your algorithm visible directly on your computer, please install the python packages, all these packages can be installed using pip:
```
pip install numpy
pip install matplotlib
```
## A Example code
Please put the field.py and your python file in the same directory. And run this code.

Refer to the next section if you want a detailed explanation of each step.

```python
import numpy as np
import matplotlib.pyplot as plt
import field.Field as Field

# set canvas refresh rate
refresh_period = 0.01
num_users = 7
field = Field(num_users, 50) # The second argument specifies the food number in the field

def move(num_users):
    return np.random.randint(4, size=(num_users + 1))
    # The function returns (num_users + 1) random numbers, because the field object requires that.

im = None
(field_image, states) = field.go(move(num_users))
print(states, end='')
try:
    im = plt.imshow(field_image.reshape(100, 100), cmap='nipy_spectral')
    plt.pause(refresh_period)
    plt.draw()
except:
    pass
plt.colorbar()

while True:
    move_cmd = move(num_users)
    # move_cmd is a list with (n+1) element, where move_cmd[i] is the i-th user's movement (start from 1).
    (field_image, states) = field.go(move_cmd)
    # you get your field_image which you can plot.
    # you get a states list wherr you can know which user is alive,
    # if states[i-1] == 1, the i-th user is still alive.

    print('\r', end='')
    print(states, end='')

    try:
        im.set_data(field_image.reshape(100, 100))
        plt.pause(refresh_period)
        plt.draw()
    except:
        print()
        break
```

## Code explain

1. place the test file field.py at your working space, and create a new python file main.py

2. import modules at your main.py
```python
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import field.Field as Field
```

3. initialize your field object
```python
# set canvas refresh rate
refresh_period = 0.01
num_users = 7
field = Field(num_users, 50) # The second argument specifies the food number in the field
```

4. define your algorithm function
```python
def move(num_users):
    return np.random.randint(4, size=(num_users + 1))
    # The function returns (num_users + 1) random numbers, because the field object requires that. 
```

5. setup your canvas so that you can see something
```python
im = None
(field_image, states) = field.go(move(num_users))
print(states, end='')
try:
    im = plt.imshow(field_image.reshape(100, 100), cmap='nipy_spectral')
    plt.pause(refresh_period)
    plt.draw()
except:
    pass
plt.colorbar()
```

6. get into a infinite loop where you can start run the field
```python
while True:
    move_cmd = move(num_users)
    # move_cmd is a list with (n+1) element, where move_cmd[i] is the i-th user's movement (start from 1).
    (field_image, states) = field.go(move_cmd)
    # you get your field_image which you can plot.
    # you get a states list wherr you can know which user is alive,
    # if states[i-1] == 1, the i-th user is still alive.
```

7. in the while loop, print all users' states and show your map
```python
    print('\r', end='')
    print(states, end='')

    try:
        im.set_data(field_image.reshape(100, 100))
        plt.pause(refresh_period)
        plt.draw()
    except:
        print()
        break
```

# Detail description of Field Object

## Initialize the Field object 

You can initialize the Field object with the number of user provided. You can also change the map size. 

```python
field = Field(num_users, num_foods=2, map_size=(100, 100))
```

## run Field.go() method to start the simulation every time step

1. input arguments (```move```)

- a list of numbers (0,1,2,3) indicates the user action (corresponding to Up,Right,Down,Left). Please add a dummy number at the front of the list, whose length should be (n+1). Then the number of ```move[i]``` indicates the ```i```-th user's action

2. return values

- ```field_image``` (the 0-th element): is the numpy array which has size that you specified, or ```100 * 100``` by default. Since the image is a numpy array, each pixel with value ```2*i``` is the i-th user's head, and ```2*i-1``` is the i-th user's body.

- ```states``` (the 1-th element): is a list of 0 or 1, which indicates dead or alive of each user. the i-th user's state is in ```states[i-1]```

# 教程

![](./localDemo.gif)

## 安装

为了使你的算法能直接在你的计算机上运行，请确保你已成功安装依赖包；你可以通过 pip 来安装：

```
pip install numpy
pip install matplotlib
```

## 例程

这是一段帮助你熟悉的例程，如果你想知道每一步具体的作用，请参阅下一个部分. 如果你想直接运行，请确保field.py与你自己的python脚本在同一目录下.

```python
import numpy as np
import matplotlib.pyplot as plt
import field.Field as Field

# set canvas refresh rate
refresh_period = 0.01
num_users = 7
field = Field(num_users, 50) # The second argument specifies the food number in the field

def move(num_users):
    return np.random.randint(4, size=(num_users + 1))
    # The function returns (num_users + 1) random numbers, because the field object requires that.

im = None
(field_image, states) = field.go(move(num_users))
print(states, end='')
try:
    im = plt.imshow(field_image.reshape(100, 100), cmap='nipy_spectral')
    plt.pause(refresh_period)
    plt.draw()
except:
    pass
plt.colorbar()

while True:
    move_cmd = move(num_users)
    # move_cmd is a list with (n+1) element, where move_cmd[i] is the i-th user's movement (start from 1).
    (field_image, states) = field.go(move_cmd)
    # you get your field_image which you can plot.
    # you get a states list wherr you can know which user is alive,
    # if states[i-1] == 1, the i-th user is still alive.

    print('\r', end='')
    print(states, end='')

    try:
        im.set_data(field_image.reshape(100, 100))
        plt.pause(refresh_period)
        plt.draw()
    except:
        print()
        break
```

## 代码解释

1. 将用于测试的文件 field.py 放在你的工作目录，并创建一个新的Python文件 main.py
2. 在main.py中载入所需要的库

```python
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import field.Field as Field
```

3. 初始化你的 field 对象

```python
# set canvas refresh rate
refresh_period = 0.01
num_users = 7
field = Field(num_users, 50) # The second argument specifies the food number in the field
```

4. 定义你写的算法函数

```python
def move(num_users):
    return np.random.randint(4, size=(num_users + 1))
    # The function returns (num_users + 1) random numbers, because the field object requires that.
```

5. 装载画布使你能够看到画面

```python
im = None
(field_image, states) = field.go(move(num_users))
print(states, end='')
try:
    im = plt.imshow(field_image.reshape(100, 100), cmap='nipy_spectral')
    plt.pause(refresh_period)
    plt.draw()
except:
    pass
plt.colorbar()
```

6. 写一个无穷循环，让你的蛇在地图上奔跑起来！

```python
while True:
    move_cmd = move(num_users)
    # move_cmd is a list with (n+1) element, where move_cmd[i] is the i-th user's movement (start from 1).
    (field_image, states) = field.go(move_cmd)
    # you get your field_image which you can plot.
    # you get a states list wherr you can know which user is alive,
    # if states[i-1] == 1, the i-th user is still alive.
```

7. 在无穷循环中输出每一步所有用户的状态，刷新你的地图

```python
    print('\r', end='')
    print(states, end='')

    try:
        im.set_data(field_image.reshape(100, 100))
        plt.pause(refresh_period)
        plt.draw()
    except:
        print()
        break
```

## 更多关于Field对象的细节

### 初始化Field对象

你可以使用自己提供的数字来初始化Field对象. 你也可以改变地图的尺寸.

```python
field = Field(num_users, num_foods=2, map_size=(100, 100))
```

### 运行Field.go()方法来模拟你的每一步

1. 传入的参数(```move```)

* 一个由0,1,2,3构成的序列( list ）来表示用户的指令( 分别指代上右下左 ). 请在序列最前面添加一个“虚拟数字”来保证序列的长度是n+1，这样可以确保 ```move[i]``` 表示的是你的第 i 个指令( 虚拟号码无具体含义 )

2. 返回值

* ```field_image```( 返回的第0个元素 )：一个你指定大小的numpy数组( 默认为```100*100``` ). 由于图片是用numpy数组来表示的，每一个值为``` 2 * i ```的像素表示第i个用户的头，每个值为``` 2 * i - 1 ```的像素表示第i个用户的身体.
* ```states```( 第一个返回值 )：一个由0或1构成的序列( list ), 表示着每个用户的生死状态. 第i个用户的状态是```states[i-1]```
