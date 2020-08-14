#!/bin/sh

# This script query and kills all the orphan process on nvidia gpu
# For example, when pytorch/tensorflow multiprocess reading data was interupted
# there may be still orphan processes, whose ppid=1
# and corresponding gpu will show "??" when yanking `nvl`

# make sure there is `fuser` command in your system
# if not, then install it via `sudo apt install psmisc`
#sudo fuser /dev/nvidia*  # or: /dev/nvidia4 for card_id=4
#ps -ef | grep '19561' | awk '{print $1, $2, $3}'
#sudo kill -9 19561

main()
{
    for pid in `sudo fuser /dev/nvidia*`; do
        #echo $pid
        out=`ps -ef | grep $pid`
        user=`echo $out | awk '{print $1}'`
        pid=`echo $out | awk '{print $2}'`
        ppid=`echo $out | awk '{print $3}'`

        if [ $ppid = '1' ]; then
            echo "$user $pid $ppid"
            hh=`sudo kill -9 $pid`
        fi
    done
}

main
