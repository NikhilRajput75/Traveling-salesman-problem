from tkinter import *
from tkinter import simpledialog

root = Tk()
root.title("Travelling Sales Man")
root.geometry("+400+200")
# root.iconbitmap('logo.ico')
root.configure(padx=20)



root.update_idletasks()
NUM_OF_CITIES = simpledialog.askinteger("Travelling Sales Man", "How many places you want to visit", parent=root, minvalue=2, maxvalue=10)



input_matrix = []
DISTANCE_MATRIX = []
WAY = []
INFINITY = 1



def find_way():
    global NUM_OF_CITIES, INFINITY, WAY, DISTANCE_MATRIX

    is_selected = [False for i in range(NUM_OF_CITIES)] # vector that marks selected nodes
    is_selected[0] = True # Include node 0 in the path

    # Initialize path vector
    WAY = [0 for i in range(NUM_OF_CITIES + 1)]

    for i in range(NUM_OF_CITIES):
        selected_neighbor = 0 # at each iteration the selected node is 0
        best_distance = INFINITY # at each iteration the best distance is infinite

        for j in range(NUM_OF_CITIES):
            # if node j is not selected and the adjacency matrix is ​​different from 0 (because being 0 indicates a path from the node to itself) and the current best dis is greater than the distance of going to node j
            if not is_selected[j] and DISTANCE_MATRIX[i][j] != 0 and best_distance > DISTANCE_MATRIX[i][j]:
                selected_neighbor = j # j node is the new path
                best_distance = DISTANCE_MATRIX[i][j] # the new best distance is the distance of going to node j
                
        WAY[i+1] = selected_neighbor # Add the selected neighbor to the path
        is_selected[selected_neighbor] = True # Mark selected neighbor

# Calculate dis for selected path
def calculate_distance(way) -> float:
    global NUM_OF_CITIES, DISTANCE_MATRIX

    dis = 0

    for i in range(NUM_OF_CITIES):
        city_A = way[i] 
        city_B = way[i+1]
        dis += DISTANCE_MATRIX[city_A][city_B]
    
    return dis       

# Display path on screen
def show_way() -> None:
    global WAY

    way = ''
    for i in range(len(WAY)):
        way += ' ' + str(WAY[i]+1) + ' '
        if i != len(WAY)-1:
            way += '→'

    path_label.config(text=f"Path: {way}")


# Performing swaps to improve the solution
def swap() -> None:
    global NUM_OF_CITIES, WAY, DISTANCE_MATRIX

    way_aux = WAY[:] # copy path obtained in the first solution to an auxiliary vector
    best_distance = calculate_distance(WAY) # best current distance

    for i in range(1, NUM_OF_CITIES):
        for j in range(i+1, NUM_OF_CITIES):
            way_aux[i], way_aux[j] = way_aux[j], way_aux[i] # swap

            dis = calculate_distance(way_aux)

            if dis < best_distance:
                best_distance = dis
                WAY = way_aux[:]

 
# Store the tkinter input into distance matrix in float type
def set_distance_matrix():
    global DISTANCE_MATRIX
    for i in range(NUM_OF_CITIES):
        c = []
        for j in range(NUM_OF_CITIES):
            distance = float(input_matrix[i][j].get())
            c.append(distance)
        DISTANCE_MATRIX.append(c)    

def find_path():
    global INFINITY
    try:
        set_distance_matrix()
        for i in range(NUM_OF_CITIES):
            for j in range(NUM_OF_CITIES):
                distance = float(DISTANCE_MATRIX[i][j])
                INFINITY = INFINITY + distance

        find_way()    # Find initial solution based on nearest neighbor
        
        # Perform swaps in order to improve the solution
        # Swap method is called multiple times to further minimize costs
        for i in range(5):
            swap()

        # display results
        show_way()
        dis = calculate_distance(WAY)
        cost_label.config(text=f"Distance: {round(dis,2)}    ")

    except:
        path_label.config(text=f"")
        cost_label.config(text=f"Wrong Input", fg="#fb0b13")


# Create the entry boxes   
for x in range(1,NUM_OF_CITIES+1):
    c = []
    for y in range(1,NUM_OF_CITIES+1):
        my_entry = Entry(root)
        my_entry.grid(row=x+1, column=y, pady=10, padx=5)
        c.append(my_entry)
    input_matrix.append(c)    


head_label = Label(root, text="Enter the distances", font=('Helvetica 15 bold')).grid(row=0, columnspan=NUM_OF_CITIES+1, pady=(5,15))

city_label = Label(root, text="City", font=('default',11,'bold')).grid(row=1, column=0)
for i in range(NUM_OF_CITIES):
    city_label_h = Label(root, text=f"City {i+1}", font=('default',10,'bold')).grid(row=1, column=i+1)
    city_label_v= Label(root, text=f"City {i+1}", font=('default',10,'bold')).grid(row=i+2, column=0)

submit_button = Button(root, text="Submit", pady=5, padx=20 , cursor='hand2', command=find_path)        
submit_button.grid(row=NUM_OF_CITIES+3+1, column=0, pady=20)     

path_label = Label(root, text="", fg="#019707", font=('default',10,'bold'))
path_label.grid(row=NUM_OF_CITIES+1+1, columnspan=NUM_OF_CITIES+1, pady=(20,5))

cost_label = Label(root, text="", fg="#9400ff", font=('default',10,'bold'))
cost_label.grid(row=NUM_OF_CITIES+2+1, columnspan=NUM_OF_CITIES+1)

root.mainloop()