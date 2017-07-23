dataset=show
dataset_ori=20170117_error
IN_PATH=/samba/HDD/dataset_$dataset
workpath=`pwd`
class_max=1		#max number max class
subject_train=1 	#the subject below the class
input_list=$workpath/input_list.txt
input_list_ori=$workpath/input_list_ori.txt
output_list=$workpath/output_list_prefix.txt
#---------------------------------------------------------------
echo -----------------------------------------------------------
echo ------------------------START------------------------------
rm -rf $input_list
cp $input_list_ori $input_list
#find and create path and number to input_list
#for class in `seq 1 $class_max` 
#do	
	#printf "class_%02d\n" $class
#	for subject in `seq 1 $subject_train`
	#do
		printf "process %s/\n" $IN_PATH
		cd `printf "%s/\n" $IN_PATH`
	maxframe=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames `printf "show.avi"` | sed 's/[^=]*=//'|sed 's/[^0-9]*]//')
		path=$(pwd)
		maxframe=`expr $maxframe - 17`
		i=1
		while [ $i -lt $maxframe ]
		do
			printf "%s/show/ %d 0\n" $path $i >> $input_list
			i=`expr $i + 16`
		done	
		cd ..
#	done
#done
#copy input_list to workpath
#	cp $input_list $workpath
echo input_list create done
#---------------------------------------------------------------
echo Start create output_list
#create output_list file
echo -----------------------------------------------------------
echo -------------------------START-----------------------------
	rm -rf $output_list
#echo remove $output_list
	cp $input_list $output_list
echo -----------------------------------------------------------
#copy the inputfile to outputfile,then modify the outputfile
#echo copy  from ~/$input_list to $output_list
echo -----------------------------------------------------------
#delete the label of each line
                echo remove class_$class label at last of eachline
                sed -i "s/..$//g" $output_list
echo -----------------------------------------------------------
#modify the path of each line, aiming to output prefix,which is the dir of features stored
echo change path
        sed -i "s/dataset_$dataset_ori/output_$dataset_ori\/c3d/g" $output_list
	sed -i "s/dataset_$dataset/output_color_test\/c3d/g" $output_list
	sed -i "s/\/subject/_subject/g" $output_list
echo -----------------------------------------------------------
#modify the jpg number of each line
echo change img_number_1
        sed -i "s/\/ 1$/\/ 001/" $output_list
echo change img_number_9
        sed -i "s/\/ 9$/\/ 009/" $output_list
echo change img_number_17
        sed -i "s/\/ 17$/\/ 017/" $output_list
echo change img_number_25
        sed -i "s/\/ 25$/\/ 025/" $output_list
echo change img_number_33
        sed -i "s/\/ 33$/\/ 033/" $output_list
echo change img_number_41
        sed -i "s/\/ 41$/\/ 041/" $output_list
echo change img_number_49
        sed -i "s/\/ 49$/\/ 049/" $output_list
echo change img_number_57
        sed -i "s/\/ 57$/\/ 057/" $output_list
echo change img_number_65
        sed -i "s/\/ 65$/\/ 065/" $output_list
echo change img_number_73
        sed -i "s/\/ 73$/\/ 073/" $output_list
echo change img_number_81
        sed -i "s/\/ 81$/\/ 081/" $output_list
echo change img_number_89
        sed -i "s/\/ 89$/\/ 089/" $output_list
echo change img_number_97
        sed -i "s/\/ 97$/\/ 097/" $output_list
echo change img_number_hudreds+
        sed -i "s/\/ /\/000/" $output_list
echo -----------------------------------------------------------
echo ------------------Start create mkdir.sh--------------------
#create mkdir.sh
	rm -rf $workpath/mkdir.sh
	cp $output_list ./dirlist.txt
        sed -i "s/^/mkdir -p /g" dirlist.txt	#insert command "mkdir -p"
        sed -i "s/......$//g" dirlist.txt	#modify path of mkdir.sh
        sort dirlist.txt | uniq >> $workpath/mkdir.sh
        rm dirlist.txt
	#cp $output_list $workpath
	
	#rm -rf $output_list 
	#rm -rf $input_list
