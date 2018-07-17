package main

import (
	"crypto/sha256"
	"fmt"
	"os"
	"strconv"
)

func check(chaine string, difficulte int) bool {
	var hash = sha256.Sum256([]byte(chaine))
	for i := 0; i < difficulte; i++ {
		if hash[i] != 0 {
			return false
		}
	}
	return true
}

func checkFichier(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	fichier, err := os.Create("test")
	check_fichier(err)
	defer fichier.Close()
	var chaine = "Satoshi Nakamoto"
	for i := 0; i < 10000; i++ {
		var _chaine = chaine + strconv.Itoa(i)
		if check(_chaine, 1) {
			fmt.Println(i)
			var res = strconv.Itoa(i)
			fichier.WriteString(res)
			fichier.Sync()
		}
	}
}
