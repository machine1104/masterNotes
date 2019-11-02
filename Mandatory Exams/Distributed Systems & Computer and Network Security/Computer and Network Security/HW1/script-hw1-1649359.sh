#!/bin/bash

PASSWORD="passwordmoltosicura"
OUTPUT="result.hw1-1649359.csv"
CICLI=10
type nul > $OUTPUT

echo ++++++ HOMEWORK 1 ++++++

for cipher in aes-256-cbc aes-256-ecb camellia-256-cbc camellia-256-ecb aria-256-cbc aria-256-ecb des-cbc des-ecb
do
    echo $cipher >>  $OUTPUT
    echo +++++ CIPHER $cipher +++++    
    for size in 100K 1MB 10MB 100MB
    do
        echo +++++ FILE SIZE $size +++++
        echo ===== ENCRYPTION =====       
        
        runtime=0
        for i in {1..$CICLI}
        do
            start=$(date +%s%N)
            openssl $cipher -a -salt -pbkdf2 -in "$size.file" -out "$size.enc" -pass pass:$PASSWORD
            runtime="$(($runtime+($(date +%s%N)-$start)))"       
           
        done

        enc_runtime_scaled=$(bc <<< "scale=3;$runtime/$CICLI/1000000")
        echo ENC_SPEED $enc_runtime_scaled

        echo ===== DECRYPTION =====       
        
        runtime=0
        for i in {1..$CICLI}
        do
            start=$(date +%s%N)
            openssl $cipher -d -a -salt -pbkdf2 -in "$size.enc" -out "$size.new.file" -pass pass:$PASSWORD
            runtime="$(($runtime+($(date +%s%N)-$start)))"       
           
        done

        dec_runtime_scaled=$(bc <<< "scale=3;$runtime/$CICLI/1000000")
        echo DEC_SPEED $dec_runtime_scaled
        echo $size >> $OUTPUT
        echo ENC";"$enc_runtime_scaled >> $OUTPUT
        echo DEC";"$dec_runtime_scaled >> $OUTPUT

        
              
    done    
done

