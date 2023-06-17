function bs_get_colour
    switch (hostname)
        case rpi
            echo D56 # pinkish-red, like a raspberry?
        case penguin
            echo F92 # historically golden-orange
        case ekhtarro
            echo 82D # imperial purple
    end
end

set -g bs_colour_host (bs_get_colour)
