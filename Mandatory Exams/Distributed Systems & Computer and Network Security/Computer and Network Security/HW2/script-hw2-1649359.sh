!/bin/bash

echo ++++++ HOMEWORK 2 ++++++
start=$(date +%s)
for dict in en it
do
    while read -r line
    do
        echo -e $line
        openssl aes-192-cbc -d -in "ciphertext-hw2-1649359.enc" -out "plaintext.txt" -pass pass:$line -pbkdf2 2> /dev/null
        if [[ $(file plaintext.txt | cut -d' ' -f2) == "ASCII" ]];
        then  
            runtime=$(($(date +%s)-$start))
            printf "La passowrd è $line\n"            
            printf "Daje! Hai sprecato ben %dh:%dm:%ds. della tua vita\n" $(($runtime/3600)) $(($runtime%3600/60)) $(($runtime%60))     
            exit
        fi
    done < "$dict-prova.txt"
done
