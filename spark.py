from __future__ import absolute_import

import argparse
from pyspark import SparkContext
from icor_mep import icor_mep


class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        return self.start <= float(other) <= self.end

    def __repr__(self):
        return "{0} - {1}".format(self.start,self.end)


if __name__ == "__main__":

    ap = argparse.ArgumentParser(description="iCOR on MEP")

    ap.add_argument("--data_type", choices=['S2','L8'], metavar="DATATYPE", help="Sentinel 2 or Landsat-8. Values : S2 or L8", required=True )
    ap.add_argument("--cloud_low_band",choices=['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B10','B11','B12'], metavar="CLDLOWBAND",  help="Band to apply cloud low threshold (zero based)." , required=True)
    ap.add_argument("--water_band", choices=['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B10','B11','B12'],metavar="WATERBAND",  help="Water detection band id (zero based)." , required=True)

    ap.add_argument("--cloud_average_threshold" , choices=[Range(0.0,1.0)] ,metavar="CLDAVGTHRSH",  help="Upper threshold with average in the visual bands to be detected as cloud." , required=True)
    ap.add_argument("--cloud_low_threshold" , choices=[Range(0.0,1.0)] ,metavar="CLDLOWTHRSH",  help="Low band threshold to be detected as cloud." , required=True)
    ap.add_argument("--aot_window_size", type=int, metavar="AOTWINDOW",  help="Square window size in pixels to perform aot estimation" , required=True)

    ap.add_argument("--water_threshold", choices=[Range(0.0,1.0)], metavar="WATERTHRSHD",  help="Water detection threshold." , required=True)

    ap.add_argument("--cirrus", choices=['true','false'] ,metavar="CIRRUS",  help="Use cirrus band for cloud detection. Value : true or false" , required=True)
    ap.add_argument("--aot", choices=['true','false'],metavar="AOT",  help="Apply AOT retrieval algorithm. Value : true or false", required=True )
    ap.add_argument("--simec", choices=['true','false'],metavar="SIMEC",  help="Apply adjacency correction. Value : true or false", required=True )
    ap.add_argument("--watervapor", choices=['true','false'],metavar="WATERVAPOR",  help="Apply watervapor estimation. Value : true or false", required=True )
    ap.add_argument("--bg_window", type=int, metavar="BG_WINDOW", help="Default background window size", required=True )
    ap.add_argument("--cirrus_threshold", choices=[Range(0.0,1.0)] , metavar="CIRRUSTHRESHOLD",  help="Cloud mask threshold value", required=True )
    ap.add_argument("--aot_override", choices=[Range(0.0,1.2)], metavar="AOT_OVERRIDE",  help="AOT override values", required=True )
    ap.add_argument("--ozone_override" , choices=[Range(0.25,0.5)], metavar="OZONE_OVERRIDE",  help="OZONE override values", required=True )
    ap.add_argument("--wv_override", choices=[Range(0.0,5.0)], metavar="WV_OVERRIDE",  help="WATERVAPOR override value", required=True )

    ap.add_argument("products", metavar="PROD", nargs="+", help="An input product archive")

    args = ap.parse_args()

    sc = SparkContext(appName='icor-mep')
    productsRDD = sc.parallelize(args.products)

    productsRDD.foreach(lambda product: icor_mep.process_product(product, args))
