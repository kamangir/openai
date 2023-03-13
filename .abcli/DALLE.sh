#! /usr/bin/env bash

function DALL-E() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == help ] ; then
        abcli_show_usage "DALL-E render <filename>$ABCUL[brush=tiling|randomwalk,~dryrun,lines=<5>,verbose]" \
            "render <filename>."
        return
    fi

    if [ "$task" == render ] ; then
        local filename=$2

        local options=$3
        local brush=$(abcli_option "$options" brush tiling)
        local lines=$(abcli_option "$options" lines -1)
        local verbose=$(abcli_option_int "$options" verbose 0)
        local dryrun=$(abcli_option_int "$options" dryrun 1)

        python3 -m openai_cli.DALLE \
            render \
            --filename $filename \
            --brush $brush \
            --dryrun $dryrun \
            --lines $lines \
            --verbose $verbose \
            "${@:4}"

        return
    fi

    abcli_log_error "-DALLE: $task: command not found."
}