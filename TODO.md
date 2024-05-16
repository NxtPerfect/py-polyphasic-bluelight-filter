- [x] How to know if we missed a section already
    - if current time > time but < next time
    - get current time and target time
        then sleep for tt-15m
        if that time is reached
- [x] ensure correct time isn't missed
- [x] properly read all the sections from json
- [x] what should the program do if time is missed or it's run in between
- [ ] Once we pass the datetime, we never go to the next one
    - should set flag, if we finished the target
    then get next section, if out of bounds, go to first 
