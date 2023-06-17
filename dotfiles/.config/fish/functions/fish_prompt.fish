function fish_prompt --description 'Informative prompt'
    #Save the return status of the previous command
    set -l last_pipestatus $pipestatus
    set -lx __fish_last_status $status # Export for __fish_print_pipestatus.

    set -l gap (set_color normal)' '

    # last cmd/pipe status
    set -l status_color (set_color $fish_color_status)
    set -l statusb_color (set_color --bold $fish_color_status)
    set -l pipestatus_string (__fish_print_pipestatus "[" "]" "|" "$status_color" "$statusb_color" $last_pipestatus)

    # Color the prompt differently when we're root
    set -l color_cwd $fish_color_cwd
    set -l suffix '> '
    if functions -q fish_is_root_user; and fish_is_root_user
        if set -q fish_color_cwd_root
            set color_cwd $fish_color_cwd_root
        end
        set suffix '# '
    end

    # Color the hostname differently for each known computer
    if not set -q bs_colour_host
        set bs_colour_host normal
    end

    echo
    echo -n -s \
        (set_color brblack) '[' (date "+%H:%M:%S") ']' $gap \
        (set_color --bold $bs_colour_host) (whoami) '@' (prompt_hostname) $gap \
        (set_color $color_cwd) (prompt_pwd) $gap \
        $pipestatus_string \
        (set_color normal) $suffix
end
