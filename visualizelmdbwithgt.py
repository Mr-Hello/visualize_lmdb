# -*- coding: utf-8 -*
import caffe
import lmdb
import numpy as np
import cv2
from caffe.proto import caffe_pb2
import time
 
lmdb_env = lmdb.open('test_lmdb')
 
lmdb_txn = lmdb_env.begin()                                 # 生成处理句柄
lmdb_cursor = lmdb_txn.cursor()                             # 生成迭代器指针
annotated_datum = caffe_pb2.AnnotatedDatum()                # AnnotatedDatum结构
 
for key, value in lmdb_cursor:
    print key
 
    annotated_datum.ParseFromString(value)
    datum = annotated_datum.datum                           # Datum结构
    grps = annotated_datum.annotation_group                 # AnnotationGroup结构
    type = annotated_datum.type
    name=key.lsplit("/",1)[1]
    image_data = np.fromstring(datum.data, dtype=np.uint8)      # 字符串转换为矩阵
    image = cv2.imdecode(image_data, -1)  
    for grp in grps:
    print "label:", grp.group_label

    	for g in grp.annotation:
	        xmin = g.bbox.xmin * datum.width           # 取到每张图片中的每个框
	        ymin = g.bbox.ymin * datum.height
	        xmax = g.bbox.xmax * datum.width
	        ymax = g.bbox.ymax * datum.height
 
        print "bbox:", xmin, ymin, xmax, ymax                      # object的bbox标签
 		cv2.rectangle(im,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,0),3) #图片上画出框

 	if ymin >10:
 		cv2.putText(im, name, (int(xmin),int(ymin-6)), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5, (0, 255, 0) )
 	else:
 		cv2.putText(im, name, (int(xmin),int(ymin+15)), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5, (0, 255, 0) )
 	cv2.imshow("image", image)								#显示图片
 	time.sleep(1)

    label = datum.label                                      # Datum结构label以及三个维度   
    channels = datum.channels
    height = datum.height
    width = datum.width
 
    print "label:", label
    print "channels:", channels
    print "height:", height
    print "width:", width

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
