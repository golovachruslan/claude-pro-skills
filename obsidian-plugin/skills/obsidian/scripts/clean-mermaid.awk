#!/usr/bin/awk -f
# clean-mermaid.awk
# Removes blank lines within Mermaid code blocks
# Usage: awk -f clean-mermaid.awk input.md > output.md

/^```mermaid/ {
    in_mermaid = 1
    print
    next
}

/^```$/ && in_mermaid {
    in_mermaid = 0
    print
    next
}

in_mermaid {
    # Only print non-blank lines within Mermaid blocks
    if ($0 !~ /^[[:space:]]*$/) {
        print
    }
    next
}

# Print all other lines unchanged
{
    print
}
