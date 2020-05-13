#WORK_PATH="/home/thk/Downloads/faster_rcnn_inception_v2_coco_2018_01_28/"
WORK_PATH="/home/thk/Downloads/faster_rcnn_resnet50_coco_2018_01_28/"
python tf_text_graph_faster_rcnn.py \
	--input ${WORK_PATH}frozen_inference_graph.pb \
  	--output ${WORK_PATH}frozen_inference_graph.pbtxt \
    	--config ${WORK_PATH}pipeline.config
