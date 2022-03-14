from threading import Event, Thread

global true_conditions
true_conditions = 0

locker = Event()


def Node_Thread(locker):
    locker.clear()  # To prevent looping, see manual, link below
    locker.wait(2.0)  # Suspend the thread until woken up, or 2s timeout is reached
    if not locker.is_set():  # when is_set() false, means timeout was reached
        print("TIMEOUT")
    else:
        print(str(true_conditions) + " continuing...")
        print("continuing...")
    #
    # Code when some conditions are true
    #


worker_thread = Thread(target=Node_Thread, args=(locker,))
worker_thread.start()

cond1 = False
cond2 = False
cond3 = False


def evaluate():
    true_conditions = 0

    for i in range(1, 4):
        if globals()["cond" + str(i)]:  # access a global condition variable one by one
            true_conditions += 1  # increment at each true value
    if true_conditions > 1:
        locker.set()  # Resume the worker thread executing the else branch
    # Or just if true_conditions > 1: locker.set();
    # true_conditions would need be incremented when 'True' is written to any of those variables


#
# some condition change code

#

evaluate()
