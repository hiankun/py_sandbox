# bash merge_dir.sh dir01/* dir02/* dirN/* merged_dir
arg_n=${#@}
target=${@: -1}
for f in ${@: 1:$arg_n-1}; do
    ext=$(file --mime-type $f | cut -d ':' -f 2 | cut -d '/' -f 2);
    mv -nv $f $target/$(md5sum -b "$f" | cut -d ' ' -f 1).$ext;
done
