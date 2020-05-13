WORK_PATH="/home/thk/Downloads/mask_rcnn_inception_v2_coco_2018_01_28/"
python3 mask_rcnn.py \
	--model ${WORK_PATH}frozen_inference_graph.pb \
	--config ${WORK_PATH}frozen_inference_graph.pbtxt \
	--classes models/coco_labels.txt \
	--colors models/coco_colors.txt
# Run ./tools/run_tf_text_graph_mask_rcnn.sh to get the pbtxt
