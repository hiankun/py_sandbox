#WORK_PATH="/media/thk/workspace/gitlab_proj/tf_model_train/trained/20200407/tuna_ssd_incep_v2_200k_frozen/"
WORK_PATH="/home/thk/Downloads/ssd_inception_v2_coco_2018_01_28/"
python tf_text_graph_ssd.py \
	--input ${WORK_PATH}frozen_inference_graph.pb \
  	--output ${WORK_PATH}frozen_inference_graph.pbtxt \
    	--config ${WORK_PATH}pipeline.config

    	#--config /media/thk/workspace/gitlab_proj/tf_model_train/trained/20200407/ssd_inception_v2_coco.config

