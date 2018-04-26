#Testing numpy
import numpy
img = Image.open("baest.jpg").convert('RGB')
arr = np.array(np.asarray(img))

R = [(90,130),(60,150),(50,210)]
red_range = np.logical_and(R[0][0] < arr[:,:,0], arr[:,:,0] < R[0][1])
green_range = np.logical_and(R[1][0] < arr[:,:,0], arr[:,:,0] < R[1][1])
blue_range = np.logical_and(R[2][0] < arr[:,:,0], arr[:,:,0] < R[2][1])
valid_range = np.logical_and(red_range, green_range, blue_range)

arr[valid_range] = 200
arr[np.logical_not(valid_range)] = 0

outim = Image.fromarray(arr)
outim.save("baestout.jpg")
