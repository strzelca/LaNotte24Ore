#!/bin/sh

# if argument debug is passed, then run in debug mode, otherwise run in production mode
if [ "$1" = "debug" ]; then
    # run npm run dev and python app.py
    echo "Running in debug mode"
    npm run dev &
    CSS_BUILD_PID=$!
    python run.py
    # close the npm run build process when python app.py is done
    kill $CSS_BUILD_PID
else
    echo "Running in production mode"
    # npm run build in one process and python app.py in another
    npm run build &
    CSS_BUILD_PID=$!
    python app.py
    # close the npm run build process when python app.py is done
    kill $CSS_BUILD_PID
fi

