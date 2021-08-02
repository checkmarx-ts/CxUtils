[ "$#" -ne 0 ] && { ( $@ ); exit; }

[ -z $TARGET_BRANCH ] && TARGET_BRANCH='master'
[ -z $CX_PRESET ] && CX_PRESET='All'
[ -z $HASH_STEP ] && HASH_STEP=10

# Clone the branch locally.
git clone --single-branch --branch $TARGET_BRANCH $GIT_URL /code

pushd /code
# Get the commits in reverse order
git log --oneline --reverse | sed -r 's/^([a-z0-9]+?)\s{1}.*$/\1/g' > /branches.txt

((count=0))

[ ! -z $START_HASH ] && ((skip=1)) || ((skip=0))

for HASH in $(cat /branches.txt)
do

    if [ $skip -ne 0 ];
    then
        if [ $HASH == $START_HASH ];
        then
            ((skip=0))
            echo Starting at next commit after $HASH
        fi
        continue
    fi

    ((check=count%$HASH_STEP))
    ((count = count + 1))

    if [ $check -ne 0 ];
    then
        echo Skipping $HASH
        continue
    fi

    echo
    echo ------ HASH: $HASH
    echo ------ PROJECT: $CX_PROJECT

    git checkout $HASH
     
    /opt/cxcli/runCxConsole.sh Scan \
    -cxuser "$CX_USER" \
    -cxpassword "$CX_PASSWORD" \
    -cxserver "$CX_SERVER" \
    -projectname "$CX_PROJECT" \
    -locationtype folder \
    -locationpath "/code" \
    -preset "$CX_PRESET" \
    -comment "Hash: $HASH" \
    -enableOsa \
    -OsaLocationPath "/code" \
    -executepackagedependency


    git checkout -- /code
    git checkout $TARGET_BRANCH 

    export HASH=""

done


