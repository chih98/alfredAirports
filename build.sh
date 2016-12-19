OUTPUT=$(python build/packageWorkflow.py . -o build/)
#OUTPUT="Airport_Search Airport_Search-0.6.22.alfredworkflow 0.6.22"

TEXT_ARRRAY=($OUTPUT)


echo ${TEXT_ARRRAY[0]}
echo ${TEXT_ARRRAY[1]}
echo ${TEXT_ARRRAY[2]}


# Do you want to git?

# https://github.com/repos/jeeftor/alfredAirports/releases

# POST /repos/:owner/:repo/releases

# {
#   "tag_name": "v1.0.0",
#   "target_commitish": "master",
#   "name": "v1.0.0",
#   "body": "Description of the release",
#   "draft": false,
#   "prerelease": false
# }

echo "     ________                               __   _______ __ "
echo "    / ____/ /_  ____ _____  ____ ____  ____/ /  / ____(_) /__  _____ "
echo "   / /   / __ \/ __ \`/ __ \/ __ \`/ _ \/ __  /  / /_  / / / _ \/ ___/ "
echo "  / /___/ / / / /_/ / / / / /_/ /  __/ /_/ /  / __/ / / /  __(__  ) "
echo "  \____/_/ /_/\__,_/_/ /_/\__, /\___/\__,_/  /_/   /_/_/\___/____/ "
echo "                         /____/ "
echo ""

git status -s

echo " Commit and make a release?"

read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # do dangerous stuff
    
    git add -u
    git commit -m "Prepping release ${TEXT_ARRRAY[2]}"
    git push

    python release.py ${TEXT_ARRRAY[2]} ${TEXT_ARRRAY[1]}
fi