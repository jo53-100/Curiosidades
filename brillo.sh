#!/bin/bash

#Mi primer script!!!
	# es un simple programa para ajustar el brillo usando ddcutil

brillo_actual() { ## Este extrae el valor actual del brillo
	ddcutil getvcp 10 | grep -o 'current value = *[0-9]\+' | grep -o '[0-9]\+'
}

actual=$(brillo_actual)

if [ $# -eq 0 ]; then
	# Cuando no hay argumentos (o sea, cuando no escribes un número)
	# el comando enseña el brillo actual
	echo "Brillo actual: $actual"

elif [ $# -eq 1 ] && [[ "$1" =~ ^[0-9]+$ ]] && [ "$1" -ge 0 ] && [ "$1" -le 100 ]; then
	# Si hay un argumento válido 
	# (o sea, que escribiste el comando
	# acompañado de un número entre 0 y 100)

	nuevo_valor=$1

	ddcutil setvcp 10 $nuevo_valor
	echo "Brillo ajustado de $actual a $nuevo_valor"

else 				# Cualquier otro caso
	echo "así no se usa, mijo."
	echo "Uso: brillo [0-100]"
	exit 1
fi

