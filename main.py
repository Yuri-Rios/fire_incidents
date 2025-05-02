from pyspark.sql import SparkSession

# Cria a sessão do Spark
spark = SparkSession.builder \
    .appName("StandaloneTest") \
    .master("local[*]") \
    .getOrCreate()

# Cria DataFrame em memória
data = [("Alice", 30), ("Bob", 25), ("Carol", 40)]
df = spark.createDataFrame(data, ["name", "age"])

# Mostra o conteúdo no terminal
df.show()

# Encerra o Spark
spark.stop()
