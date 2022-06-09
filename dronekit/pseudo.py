
acc_data =[]
acc_data = threading_func()
THRESHOLD = 8.8
while True:

    if acc_data[-1] < THRESHOLD:
        
        # deploy arms
        spin_servo()

        # bring to hover 
        dronekit.hover()

        # land 
        dronekit.land()

        break

write_to_file(acc_data)


    