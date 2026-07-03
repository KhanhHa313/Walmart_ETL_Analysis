import schedule 
import time
from main import main

analysis = schedule.every(5).seconds.do(main).tag("analysis")

start_time = time.time()


while True: 
    schedule.run_pending()
    time.sleep(1)

    if time.time() - start_time > 10: # run for more than 30 seconds since the start
        schedule.cancel_job(analysis)
        break

# schedule.cancel_job(analysis)
# schedule.clear("analysis")
# schedule.clear()

if __name__ == "__main__":
    main()