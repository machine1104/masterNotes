!/bin/bash

echo ++++++ HOMEWORK 2 ++++++
start=$(date +%H%M%S%N)
for dict in en
do
    while read -r line
    do
        echo -e $line
        openssl aes-192-cbc -d -in "ciphertext-hw2-1649359.enc" -out "plaintext.txt" -pass pass:$line -pbkdf2 2> /dev/null
        if [[ $(file plaintext.txt | cut -d' ' -f2) == "ASCII" ]];
        then  
            echo DAJE
            end=$(date +%H%M%S%N)
            runtime="$(bc <<< "scale=3;$end-$start")"
            runtime_scaled=$(bc <<< "scale=3;$runtime/1000000")
            echo $runtime_scaled       
            exit
        fi
    done < "$dict-hw2-1649359.dic"
done
