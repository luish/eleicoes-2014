#!/bin/bash

# TODO:
# Convert files to UTF-8
# Command: iconv -f ISO-8859-1 -t utf-8 old-file.csv > new-file.csv

folder="data/candidatos/csv/"

estados="AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO"
cargos=("gov" "vice_gov" "sen" "sen_sup_1" "sen_sup_2" "dep_fed" "dep_est")
cargos_ids=(3 4 5 9 10 6 7)

build_url() {
    base_url="http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{UF}/candidatos/cargo/{CARGO}/downloadCSV"
    echo $base_url | sed "s/{UF}/$1/" | sed "s/{CARGO}/$2/"
}

for estado in $estados
do
    estado_folder="${folder}${estado}/"
    mkdir -p $estado_folder

    i=0
    for cargo in ${cargos[*]}
    do
        filename="${estado_folder}${cargo}.csv"
        url=$(build_url ${estado} ${cargos_ids[$i]})
        i=$(expr $i + 1)

        curl -s -o $filename $url
        
        echo "Saved file $filename"
    done
done

# BR
curl -s -o "${folder}BR/presidente.csv" $(build_url BR 1)
curl -s -o "${folder}BR/vice-presidente.csv" $(build_url BR 2)
