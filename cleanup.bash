#  Rename survey file.
mv surveys.txt fullsurveys.txt

#  Remove spaces in file names, replace with underscores.
for file in /Users/elizabeth/Documents/Analysis/pinglogs/*[0-9]; do mv "$file" "`echo $file | sed -e 's, ,_,g'`"; done

#  Remove pinglogs with error phrases.
grep -rnwl '/Users/elizabeth/Documents/Analysis/pinglogs' -e "ERROR" | xargs rm

#  Find all survey lines with AC (Adobe Connect) , pipe to file.
grep -r '/Users/elizabeth/Documents/Analysis/fullsurveys.txt' -e "ACPilot" > ACPilotsurveys.txt

#  Remove all AC Pilot survey results from surveys.txt.
grep -v '/Users/elizabeth/Documents/Analysis/fullsurveys.txt' -e "ACPilot" > surveys.txt

#  Remove pinglogs from before 10/1/14.
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Cabrillo_9-5-2014_9.30
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Nimitz_9-8-2014_11.41
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-5-2014_9.11
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_11.24
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_11.45
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_13.47
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_13.50
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_14.2
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_20.51
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_8.36
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_9.47
rm -f /Users/elizabeth/Documents/Analysis/pinglogs/Testing_9-8-2014_9.53

#  Clean up IBL date bug.
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_10_40_11-14-2014_1.51	/Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_10_40_11-13-2014_1.51
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_11_30_11-14-2014_2.29 /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_11_30_11-13-2014_2.29
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_2_20_11-14-2014_5.27 /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_2_20_11-13-2014_5.27
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_9_50_11-14-2014_1.21 /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_9_50_11-13-2014_1.21
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_10_40_11-21-2014_1.40	/Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_10_40_11-20-2014_1.40
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_11_30_11-21-2014_3.3 /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_11_30_11-20-2014_3.3
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_2_20_11-21-2014_5.30 /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_2_20_11-20-2014_5.30
mv /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_9_50_11-21-2014_0.52 /Users/elizabeth/Documents/Analysis/pinglogs/IBL_Thurs_9_50_11-20-2014_0.52


#  Pipe remaining files to a list for use in the main program.
temp=$(find /Users/elizabeth/Documents/Analysis/pinglogs/*[0-9] | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ',')
temp2=$(echo "$temp" | rev | cut -c 2- | rev)
echo 'pingfiles = ['$temp2']' > pingfilelist.py

#  Pipe blackbox files to a list for use in the main program

temp=$(find /Users/elizabeth/Documents/Analysis/pinglogs/testbox/*/*/* | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ',')
temp2=$(echo "$temp" | rev | cut -c 2- | rev)
echo 'testblackboxpingfiles = ['$temp2']' > testboxfilelist.py

temp=$(find /Users/elizabeth/Documents/Analysis/pinglogs/pilot-ibl/*/*/* | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ',')
temp2=$(echo "$temp" | rev | cut -c 2- | rev)
echo 'iblblackboxpingfiles = ['$temp2']' > iblblackboxfilelist.py

temp=$(find /Users/elizabeth/Documents/Analysis/pinglogs/pilot-slhs/*/*/* | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ',')
temp2=$(echo "$temp" | rev | cut -c 2- | rev)
echo 'slhsblackboxpingfiles = ['$temp2']' > slhsblackboxfilelist.py

temp=$(find /Users/elizabeth/Documents/Analysis/pinglogs/pilot-sierramont/*/*/* | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ',')
temp2=$(echo "$temp" | rev | cut -c 2- | rev)
echo 'sierramontblackboxpingfiles = ['$temp2']' > sierramontblackboxfilelist.py