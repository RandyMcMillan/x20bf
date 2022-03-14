#!/bin/sh
# getopts code adapted from http://mywiki.wooledge.org/BashFAQ/035#getopts

show_help() {
cat << HELP
Usage: $(basename "$0") [-h] [-s SYNTAX] [-t TITLE] [-e EXPIRY]
Send stdin to dpaste.com, optionally setting syntax/title/expiry.
Resulting item will be opened in your browser.

If DPASTE_API_TOKEN is set in the environment, it will be used
for authentication.
HELP
}

# Set User-Agent header, per dpaste.com TOS
params="-A 'dpaste.sh'"

while getopts hs:t:e: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        s)  params="$params -F syntax=$OPTARG"
            ;;
        t)  params="$params -F title=$OPTARG"
            ;;
        e)  params="$params -F expiry_days=$OPTARG"
            ;;
        *)
            show_help >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))"

echo "Paste your content now, ^D to submit."

# Make the API call, passing stdin to 'content' param
if [ -z $DPASTE_API_TOKEN ]
then
    url=$(curl -s -F "content=<-" $params http://dpaste.com/api/v2/)
else
    echo "(Using DPASTE_API_TOKEN from environment)"
    url=$(curl -s -H "Authorization: Bearer $DPASTE_API_TOKEN" -F "content=<-" $params https://dpaste.com/api/v2/)
fi

echo "---"
echo $url

# Open in browser
if [ -x "$(command -v xdg-open)" ];
then
    xdg-open $url
else
    open $url
fi