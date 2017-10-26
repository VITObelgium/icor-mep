#!/bin/sh

if [ "$#" -lt 1 ]; then
  echo "Usage: run-cluster-s2.sh product [product ...]"
  exit 1
fi

zip -r icor_mep.zip icor_mep/ && \
spark-submit --master yarn-cluster --executor-memory 3G --conf spark.shuffle.service.enabled=true \
                                        --conf spark.dynamicAllocation.enabled=true --py-files icor_mep.zip spark.py \
                                        --cloud_average_threshold 0.19 --cloud_low_band B01 \
                                        --cloud_low_threshold 0.25 --cirrus true --aot true \
                                        --aot_window_size 100 --simec true --watervapor false \
                                        --bg_window 1 --cirrus_threshold 0.01 --aot_override 0.1 \
                                        --ozone_override 0.33 --wv_override 2.0 --water_band B08 \
                                        --water_threshold 0.05 --data_type S2 $@
