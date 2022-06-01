#!/bin/bash
# Written on: 2022.6.1 
# Author: PokeyBoa
#
# Compatibility: Available for MacOS and Linux (CentOS/Debian)
#

# set -o nounset                                # Referencing an undefined variable will throw an error / set -u
# stty erase '^h'                               # Backspace key operation
# trap 'echo -e "  \nGoodbye...\n"' EXIT        # SIGINT signal capture
export LANG=en_US.UTF-8                         # Set the locale
datesuf=`date +%Y%m%d`                          # Date suffix
symbols=`perl -e "print '#' x 50;"`             # Dividing line
currentdir=`cd $(dirname $0); pwd`              # Script's current path
basedir=`dirname $currentdir`"/"                # Script's parent path
filename=`basename $0`                          # Script's file name


# Convert dash to bash interpreter
# ls -l /bin/sh | grep -qi "dash" && ln -fs /bin/bash /bin/sh

# Determine the system platform type
# hostinfo 2> /dev/null | grep -qi "Darwin"
# if [ $? -eq 0 ]; then
#     os_platform="macos"
# else
#     if [ -f /etc/os-release ]; then
#         release=`awk 'BEGIN { FS="\""; OFS="" } /PRETTY_NAME/{ val=$(NF-1) } END { split(val, a, fs=" "); print(tolower(a[1])) }' /etc/os-release`
#         if [ ${release} == "centos" ] || [ ${release} == "debian" ]; then
#             os_platform="linux"
#         else
#             os_platform="unix-like"
#         fi
#     fi
# fi
#
# case ${os_platform} in
#     'macos')
#         # echo "mac"
#     ;;
#     'linux' | 'unix-like')
#         # echo "linux"
#     ;;
# esac


excluded_files="[^_]util.py|connect.py|__init__.py|unit_test.py|settings.py|.yml|manage.py|README.md|requirements.txt|example.py|.sh"
excluded_func="auto_connect|update|query|delete|select|FileType|FileFormat|file_exist|file_format|_advjson_dump"

listdir=`ls -lR ${basedir} | awk -v p=${basedir} '!/^total|^$|:$/{system("find "p" -type f -name *"$NF"*")}' | sort -u | egrep -v "${excluded_files}"`
setting=`find ${basedir} -type f -name "settings.py"`

routes=""
for f in ${listdir}
do
    _dir=`dirname ${f}`
    module_name=`basename "${_dir}"`
    package_name=`basename "${f}" | sed 's/.py//'`
    func_name=`cat "${f}" | egrep -i "^class|^def" | sed 's/(.*:$//; s/://; s/(//' | egrep -v "${excluded_func}" | sed 's/class //; s/def //'`
    for i in ${func_name}
    do
        routes+="    \"${module_name}.${package_name}.${i}\",\n"
    done
done

cp -a ${setting} "/tmp/settings.${datesuf}.bak"
sed -i '/INSTALLED_ROUTES/,/}/d' ${setting}
sed -i "/# Defines the loading/a\INSTALLED_ROUTES = {\n${routes}}" ${setting}

if [ -f /tmp/settings.${datesuf}.bak ]; then
    echo "function loaded successfully!"
else
    echo "..."
fi

#EOF
