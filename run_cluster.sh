#!/bin/bash

# Check for minimum number of required arguments
if [ $# -lt 3 ]; then
    echo "Usage: $0 head_node_address --head|--worker path_to_hf_home [additional_args...]"
    exit 1
fi

# Assign the first three arguments and shift them away
HEAD_NODE_ADDRESS="$1"
NODE_TYPE="$2"  # Should be --head or --worker
PATH_TO_HF_HOME="$3"
shift 3

# Additional arguments are passed directly to the Docker command
ADDITIONAL_ARGS=("$@")

# Validate node type
if [ "${NODE_TYPE}" != "--head" ] && [ "${NODE_TYPE}" != "--worker" ]; then
    echo "Error: Node type must be --head or --worker"
    exit 1
fi

# Export HuggingFace home directory as an environment variable
export HF_HOME="${PATH_TO_HF_HOME}"

# Command setup for head or worker node
RAY_START_CMD="ray start --block"
if [ "${NODE_TYPE}" == "--head" ]; then
    RAY_START_CMD+=" --head --port=6379"
else
    RAY_START_CMD+=" --address=${HEAD_NODE_ADDRESS}:6379"
fi

# Run the Ray start command
echo "Starting Ray with command: ${RAY_START_CMD}"
eval "${RAY_START_CMD} ${ADDITIONAL_ARGS[@]}"
