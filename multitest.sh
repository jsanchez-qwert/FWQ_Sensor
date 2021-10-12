python3 ./sensor.py $1:$2 tiana &
# shellcheck disable=SC2116
id_1=$(echo $!)
echo "$id_1"

python3 ./sensor.py $1:$2 Tobogan &
id_2=$(echo $!)
echo "$id_2"

python3 ./sensor.py $1:$2 Aguaparque &
id_3=$(echo $!)
echo "$id_3"

python3 ./sensor.py $1:$2 Fotos_Josefa &
id_4=$(echo $!)
echo "$id_4"

sleep 30
kill -9 "$id_1"
kill -9 "$id_2"
kill -9 "$id_3"
kill -9 "$id_4"
