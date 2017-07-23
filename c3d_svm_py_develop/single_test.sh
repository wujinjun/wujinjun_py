#!/usr/bin/env bash
mv /samba/HDD/dataset_show/*.avi /samba/HDD/dataset_show/show.avi
rm -rf /samba/HDD/dataset_show/show
rm -rf /samba/HDD/output_color_test/c3d/show/*
chmod 777 /samba/HDD/dataset_show/show.avi
./extract_frame.sh
sh create_show_list.sh
sh extract_feature.sh
python c3d_svm_predict_single.py
#rm -rf /samba/HDD/dataset_show/show
#rm -rf /samba/HDD/dataset_show/show.avi
