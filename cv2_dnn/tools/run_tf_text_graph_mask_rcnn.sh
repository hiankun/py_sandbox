WORK_PATH="/home/thk/Downloads/mask_rcnn_inception_v2_coco_2018_01_28/"
python tf_text_graph_mask_rcnn.py \
	--input ${WORK_PATH}frozen_inference_graph.pb \
  	--output ${WORK_PATH}frozen_inference_graph.pbtxt \
    	--config ${WORK_PATH}pipeline.config

    	#--config /media/thk/workspace/gitlab_proj/tf_model_train/trained/20200407/ssd_inception_v2_coco.config

