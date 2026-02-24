#!/bin/bash

echo "Iniciando..."
for i in {1..5}; do
	for x in {1..2};do
		echo -n "."
		sleep 0.5
	done
	echo ""
done
echo "PUTO EL QUE LO LEA" | cowsay

