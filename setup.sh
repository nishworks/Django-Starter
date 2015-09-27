# Make sure this script is sourced
if [[ "$(basename -- "$0")" == "setup.sh" ]]; then
    echo "Don't run $0, source it like this - source setup.sh" >&2
    exit 0
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo "setup.sh is located in $DIR"

# Deactivate if inside a virtual environment
python -c 'import sys; print sys.real_prefix' 2>/dev/null && INVENV=1 || INVENV=0
if [[ "$INVENV" == 1 ]]; then
  echo "Inside Virtual environment, deactivating.."
  deactivate
fi

# Run tox to create virtual environment and install packages
tox

# Setup alias for activating environment
alias activate='source $DIR/.tox/py27/bin/activate && echo "Activated: $(which python)"'
# Setup alias for opening docs
alias doc='open $DIR/docs/_build/html/index.html'
# Setup alias for running server in debug mode
alias run='activate && python $DIR/example_project/manage.py runserver'
# Alias for cd into project workspace
alias dspace='cd $DIR && pwd'
# Activate virtual environment
activate

# Create docs
cd docs
make html
cd ..

# Print messages
printf '\n'
echo 'Following commands are now available for this shell session:'
printf '\n'
echo '  * run         Executes python manage.py runserver -r'
echo '  * doc         Opens documentation in a browser'
echo '  * fspace      cd into this directory from anywhere'
echo '  * activate    Activates the virtual environment'
echo '  * deactivate  Deactivates the virtual environment'
printf '\nAbove commands can be run from any directory'
printf '\n\n'

# Open docs
#doc
# Open project in sublime
#subl .
# Run server
#run
