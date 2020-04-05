#!/bin/sh

. /etc/ansible/facts.d/i22_vars.sh

#Check identifying openstack servers.
[[ $SYSTEM_MANUFACTURER = "OpenStack Foundation" ]] && IS_OPENSTACK=1 || IS_OPENSTACK=0

if [ $IS_LINUX = 1 ] && [ $IS_OPENSTACK != 1 ]; then
        OUTPUT=()
        #Check to include intefaces that are confgiured with IPV6 in Centos/Redhat 6 servers(grep -B 3 UP to grep -B 5 UP)
        for i in `/sbin/ifconfig -a | grep -B 5 UP | egrep "^eth|^en" |awk '{print $1}' | cut -d ":" -f1 | uniq`
        do
                [[ $(/sbin/ethtool $i | grep "Link detected: yes" > /dev/null)$? = 0 ]] && LINK=1 || LINK=0
                [[ $(/sbin/ethtool $i | grep "Duplex: Full" > /dev/null)$? = 0 ]] && FULL=1 || FULL=0
                [[ $(/sbin/ethtool $i | grep "Speed: 1000" > /dev/null)$? = 0 ]] && SPEED=1 || SPEED=0
                if [ $LINK = 1 -a $FULL = 1 -a $SPEED = 1 ]; then
                        eval "I22_DUPLEX_${i}=1"
                else
                        eval "I22_DUPLEX_${i}=0"
                fi
                OUTPUT+=("I22_DUPLEX_${i}")
        done
        echo "{"
        crap=$(for i in "${OUTPUT[@]}"
        do
                echo -n "\"$i\": \"${!i}\", "
        done | sed 's/, $//')
        echo $crap
        echo "}"
fi

if [ $IS_SOLARIS = 1 ]; then
        OUTPUT=()
        for i in `/sbin/ifconfig -a | grep UP | grep -v lo0 | awk -F: '{print $1}'|sort|uniq`
        do
                [[ $(/usr/sbin/dladm show-dev $i | grep "duplex: full" > /dev/null)$? = 0 ]] && FULL=1 || FULL=0
                [[ $(/usr/sbin/dladm show-dev $i | grep "speed: 1000" > /dev/null)$? = 0 ]] && SPEED=1 || SPEED=0
                if [ $FULL = 1 -a $SPEED = 1 ]; then
                        eval "I22_DUPLEX_${i}=1"
                else
                        eval "I22_DUPLEX_${i}=0"
                fi
                OUTPUT+=("I22_DUPLEX_${i}")
        done
        echo "{"
        crap=$(for i in "${OUTPUT[@]}"
        do
                echo -n "\"$i\": \"${!i}\", "
        done | sed 's/, $//')
        echo $crap
        echo "}"
fi
