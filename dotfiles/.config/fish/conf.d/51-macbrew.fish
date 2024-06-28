# source homebrew env configurations if we're on an m1 mac.
if [ -d /opt/homebrew ]
    eval "$(/opt/homebrew/bin/brew shellenv)"
end
