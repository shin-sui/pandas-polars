#!/bin/bash
set -eu

ENV_FILE_PATH=./docker/.env
USERNAME_VALUE=${USERNAME:-$(whoami)}
USER_ID=1000
GROUP_ID=1000

if [[ -f ${ENV_FILE_PATH} ]]; then
	rm ${ENV_FILE_PATH}
fi

{
    echo "USERNAME=${USERNAME_VALUE}"
    echo "UID=$USER_ID"
    echo "GID=$GROUP_ID"
} >> ${ENV_FILE_PATH}


echo "Environment setup is complete!"
