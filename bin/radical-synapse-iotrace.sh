#!/bin/sh

cd /tmp
LOG=/tmp/radical.synapse.iotrace.log

if ! test -f /usr/sbin/blktrace
then
    echo "no blktrace in /usr/bin"
    exit 1
fi

cleanup()
{
    sudo killall blktrace 2>>/dev/null
    exit
}
trap cleanup EXIT QUIT TERM KILL

rm -f  $LOG
touch  $LOG

( sudo blktrace -d /dev/sda -o - \
  |      blkparse -i - -f ' ======== time:%T.%9t pid:%p action:%a rbws:%d blocks:%n size:%N \n' \
  |      grep '========' \
  > $LOG 2>&1 \
) &

tail -f $LOG

