#!/bin/bash

# Generate a random amount of game and sort the logs file into the proper folder
# Usage: ./generate_random.sh <number_of_games> <output_folder>

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: ./generate_random.sh <number_of_games> <output_folder>"
    exit 1
fi

# Check if the first argument is a number
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    echo "The first argument must be a number"
    exit 1
fi

# Create a folder for the output
rm -rf $2
mkdir $2
mkdir $2/white
mkdir $2/black
mkdir $2/draw

# Generate the random amount of games
for i in $(seq 1 $1); do
    # get who won the game
    winner=$(python main.py -w random -b random -t 60 -l $2/game_$i.txt | grep Winner | awk '{print $2}' | tr -d ',')
    # move the log file to the proper folder
    if [ "$winner" -eq 1 ] ; then
        mv $2/game_$i.txt $2/black
    elif [ "$winner" -eq -1 ] ; then
        mv $2/game_$i.txt $2/draw
    else
        mv $2/game_$i.txt $2/white
    fi
done

zip -r $2.zip $2
mv $2.zip training_zip

# Add the output folder to the .gitignore file and check if it is already in the file
grep -w $2 ../.gitignore > /dev/null
if [ $? -ne 0 ]; then
    echo $2 >> ../.gitignore
fi