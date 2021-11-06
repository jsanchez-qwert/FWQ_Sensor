python3 ./sensor.py $1:$2 D &
# shellcheck disable=SC2116
id_1=$!
echo "$id_1"

python3 ./sensor.py $1:$2 A &
id_2=$!
echo "$id_2"

python3 ./sensor.py $1:$2 B &
id_3=$!
echo "$id_3"

python3 ./sensor.py $1:$2 C &
id_4=$!
echo "$id_4"

sleep 1728000
kill -2 "$id_1"
kill -2 "$id_2"
kill -2 "$id_3"
kill -2 "$id_4"
