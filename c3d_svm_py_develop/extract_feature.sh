rm mkdir.sh
output_list=./output_list_prefix_ori.txt
cp $output_list ./dirlist.txt
sed -i "s/^/mkdir -p /g" dirlist.txt    #insert command "mkdir -p"
sed -i "s/......$//g" dirlist.txt   #modify path of mkdir.sh
sort dirlist.txt | uniq >> mkdir.sh
rm dirlist.txt
	 
sh ./mkdir.sh
rm mkdir.sh
GLOG_logtosterr=1 /home/wjj/C3D/build/tools/extract_image_features.bin prototxt/c3d_feature_extractor_frm.prototxt _iter_10000 0 50 164 ./output_list_prefix_ori.txt fc6-1 
