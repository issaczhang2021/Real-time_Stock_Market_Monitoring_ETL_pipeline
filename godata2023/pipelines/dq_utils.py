from soda.scan import Scan
from pyspark.sql import SparkSession

def spark_scan(
    df,
    spark,
    soda_check_name,
    soda_varaiables={},
    root_dir: str = '/opt/spark/work-dir/godata2023/data_quality',
):
    # Create a view that SodaCL uses as a dataset
    df.createOrReplaceTempView(soda_check_name)
    # Create a Scan object, set a scan definition, and attach a Spark session
    scan = Scan()
    scan.set_verbose(True)
    scan.set_scan_definition_name(f"scan_{soda_check_name}")
    scan.set_data_source_name(soda_check_name)
    scan.add_spark_session(spark, data_source_name=soda_check_name)
    if soda_varaiables:
        scan.add_variables(soda_varaiables)
    scan.add_sodacl_yaml_file(f"{root_dir}/{soda_check_name}.yml")
    # Execute a scan
    scan.execute()
    scan_results = scan.get_scan_results()
    print('------ Loading data validation results -----')
    print(scan.get_logs_text())
    print('------ End of data validation results -----')

    # error handling
    if scan_results.get('hasErrors') is True:
        raise Exception(
             "Soda check file has syntax errors, please check logs"
        )
    else:
        if scan_results.get("hasWarnings") is True:
            print(
                 "Soda scan is successful! There are some warnings, please"
                 " check logs"
            )
        else:
            print("Soda scan is successful! All checks passed!")
