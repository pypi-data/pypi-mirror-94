#!/usr/bin/env sh
TESTSET_PATH='qary/data/testsets'
SOLUTION_FILENAME='test_questions.solution.txt'
SOLUTION_FILEPATH="$TESTSET_PATH/$SOLUTION_FILENAME"
QUESTIONS_FILEPATH="$TESTSET_PATH/test_questions.txt"
OUTPUT_FILEPATH="$TESTSET_PATH/test_questions.output.txt"

if [ ! -f "$SOLUTION_FILEPATH" ]; then
    mkdir -p $TESTSET_PATH
    curl "https://gitlab.com/tangibleai/qary/-/raw/master/${QUESTIONS_FILEPATH}" -o $QUESTIONS_FILEPATH
    curl "https://gitlab.com/tangibleai/qary/-/raw/master/${SOLUTION_FILEPATH}" -o $SOLUTION_FILEPATH
fi

qary -s qa < "$QUESTIONS_FILEPATH" > "$OUTPUT_FILEPATH"

if [ $(diff "$OUTPUT_FILEPATH" "$SOLUTION_FILEPATH") ]; then
    exit 1
fi
