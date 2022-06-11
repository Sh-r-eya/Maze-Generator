# Maze-Generator
 
The following project is capable of generating unique mazes of varying difficulties. 
The user can attempt to solve the mazes on the screen using arrow keys. The program is also capable of saving these mazes as csv files so that the mazes can be attempted later or by a different user. 

The user interface provides a game-like experience where different users
can create separate accounts and attempt the same mazes.
 
Users can view their time taken to solve the maze and their best time at a maze of that difficulty.

## Maze Algorithm

In order to draw the maze, we have used several pygame features. The maze consists of a grid of coordinates - a 2D list in our program. After drawing the borders and openings of the maze, the remaining coordinates are filled using randomly generated snake lines.


# Snake lines:
The program creates a list of directions which represent a line that would look natural in a maze and will not form closed loops or spirals. These randomly generated lines usually resemble snakes, hence we are calling them snake lines. A random coordinate in the maze is chosen as the start point of the snake line. The general direction of the line is chosen. A snake line moving in that direction is created. The snake line is drawn until it reaches a coordinate which is already filled.

![image](https://user-images.githubusercontent.com/89849229/173179088-f988ac14-dccd-454b-ba20-f91d08a96f2c.png)


This ensures that the mazes generated by this algorithm will always have a proper solution and there will only be one solution for each maze.

# Saving a maze as a CSV:
The program also converts a maze into a csv using the pygame function window.get_at to check the colour of the point in between two coordinates, i.e. whether there is a line between all adjacent pairs of coordinates. The CSV file stores these values for each coordinate in the maze as 00, 01, 10 or 11. Where 00 represents that there is no line connecting it to the coordinate to the right or below and 01 represents that there is no line between that coordinate and the coordinate on the right but there is a line between that coordinate and the one below.

Given below is a sample maze and its corresponding save values.
![image](https://user-images.githubusercontent.com/89849229/173179174-8c2d74f2-186c-49c1-a79d-cdcd99ab80d4.png)

# Recreating mazes from csv
The program can read the csv files to recreate mazes. The mazes are saved as username_maze(date and time of creating the maze). The program uses the module
datetime for this task. If the user chooses to rename the csv files, it will not affect the program. While recreating mazes, the user can select the maze files from their device. 

# User and interface features
The user interface was created using a combination of tkinter and pygame. Users can create an account with a username and password to keep track of the mazes they attempt and improve their highscore. The user data (password and highscores) is stored in a binary file. After logging in to their account, the user can choose to generate a new maze or attempt a previously saved maze. If the player chooses to generate a new maze, they can select the difficulty of the maze to be generated. Our project creates mazes of 4 different levels of difficulty. Larger mazes are more difficult to solve, therefore, the largest mazes are level 4 and the smallest mazes are level 1.

# Solving the maze:
The user can draw a path across the maze using arrow keys. To retrace their path, the user can use backspace. However, if the user attempts to draw a line over a wall, it will result in a loss. Then the user is given the choice to try again or give up. On successfully completing a maze, the user is shown the time they have taken to solve the maze as well as their best time on a maze of that difficulty. Then, the user is given the option to save that maze.
