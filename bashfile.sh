echo "Bash version ${BASH_VERSION}..."

ndays=5

for day in {0..5}
do
  echo "Create folder $day"
  mkdir ./try/$day
done