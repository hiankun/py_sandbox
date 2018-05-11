arg_n=${#@}
target=${@: -1}
for f in ${@: 1:$arg_n-1}
    do mv -nv "$f" $target/$(md5sum -b "$f" | cut -d ' ' -f 1); 
    #do echo "$arg_n" "$f" "$target"
done
